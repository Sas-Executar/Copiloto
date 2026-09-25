from pathlib import Path
from common import load_json, save_json, process_spec

# Estados de exibição (V2.3): o progresso deixa de ser quantizado (0/33/66/99/100)
# e passa a ser a razão real de etapas HABILITADAS concluídas. O ciclo só chega a
# 100% real (EMPACOTADO) depois do empacotamento validado; antes disso, ao concluir
# a última etapa habilitada, o estado é PRONTO_PARA_EMPACOTAR — não 100%.
PLANEJANDO = "PLANEJANDO"
EM_ANDAMENTO = "EM_ANDAMENTO"
PRONTO_PARA_EMPACOTAR = "PRONTO_PARA_EMPACOTAR"
EMPACOTADO = "EMPACOTADO"


def sync_produto_condicional(state):
    """Liga/desliga as etapas do Bloco D (condicional='produto') conforme a decisão
    registrada em state['produto_esperado'] (None = ainda não decidido; nunca inferir).
    Nunca mexe em etapas já IN_PROGRESS ou DONE."""
    decisao = state.get('produto_esperado')
    for s in state['steps']:
        if s.get('conditional') != 'produto':
            continue
        if s['status'] in ('IN_PROGRESS', 'DONE'):
            continue
        if decisao is True:
            s['enabled'] = True
            if s['status'] == 'SKIPPED':
                s['status'] = 'PENDING'
        elif decisao is False:
            s['enabled'] = False
            s['status'] = 'SKIPPED'
        else:  # decisão ainda pendente: etapa existe, mas não conta e não é elegível
            s['enabled'] = False
            s['status'] = 'PENDING'
    return state


def eligible_steps(state):
    """Etapas que podem ser iniciadas agora. WIP=1: se algo está IN_PROGRESS, nada
    mais é elegível. Respeita depends_on e enabled (asset_key=0 ou Bloco D fechado)."""
    by = {s['id']: s for s in state['steps']}
    if any(s['status'] == 'IN_PROGRESS' for s in state['steps']):
        return []
    out = []
    for s in state['steps']:
        if not s.get('enabled') or s['status'] not in ('PENDING', 'READY'):
            continue
        if all(by[d]['status'] in ('DONE', 'SKIPPED') for d in s.get('depends_on', [])):
            out.append(s)
    return out


def pending_product_decision(state):
    """True quando o artigo master (S17) está concluído mas ninguém decidiu ainda
    se o CTA deste ciclo gera uma solução/produto (abre ou não o Bloco D)."""
    by = {s['id']: s for s in state['steps']}
    s17 = by.get('S17')
    return bool(s17 and s17['status'] in ('DONE', 'SKIPPED') and state.get('produto_esperado') is None)


def current_bloco(state):
    for s in state['steps']:
        if s.get('enabled') and s['status'] not in ('DONE', 'SKIPPED'):
            return s.get('bloco')
    return None


def recalc(state):
    sync_produto_condicional(state)
    enabled = [s for s in state['steps'] if s.get('enabled')]
    done = sum(1 for s in enabled if s['status'] == 'DONE')
    total = len(enabled)
    percent_real = round(100 * done / total) if total else 0

    if done == 0:
        estado = PLANEJANDO
    elif done < total:
        estado = EM_ANDAMENTO
    elif state.get('packaged'):
        estado = EMPACOTADO
    else:
        estado = PRONTO_PARA_EMPACOTAR

    state['percent'] = percent_real
    state['state'] = estado
    state['done_count'] = done
    state['enabled_count'] = total
    state['bloco_atual'] = current_bloco(state)
    state['decisao_produto_pendente'] = pending_product_decision(state)
    return state
