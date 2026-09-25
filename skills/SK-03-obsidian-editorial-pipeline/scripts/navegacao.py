from pathlib import Path
from common import load_json, arquivo_estado, arquivo_ciclo, process_spec
from state_engine import current_bloco, pending_product_decision

STATUS_PT = {"PENDING": "Pendente", "READY": "Pronta", "IN_PROGRESS": "Em andamento",
             "DONE": "Concluída", "SKIPPED": "Não aplicável", "BLOCKED": "Bloqueada"}
ICON = {"PENDING": "○", "READY": "●", "IN_PROGRESS": "▶", "DONE": "✓", "SKIPPED": "–", "BLOCKED": "!"}

BLOCO_NOME = {b['code']: b['name'] for b in process_spec()['blocos']}


def wikilink(path, label=None):
    p = str(Path(path).with_suffix('')).replace('\\', '/')
    return f"[[{p}|{label or Path(p).name}]]"


def replace_block(text, marker, content):
    a = f"<!-- {marker}:INICIO -->"
    b = f"<!-- {marker}:FIM -->"
    if a in text and b in text:
        pre, rest = text.split(a, 1)
        _, post = rest.split(b, 1)
        return pre + a + '\n' + content.strip() + '\n' + b + post
    return text


def enabled_steps(st):
    return [s for s in st['steps'] if s.get('enabled')]


def current_step(st):
    es = enabled_steps(st)
    for s in es:
        if s['status'] == 'IN_PROGRESS':
            return s
    by = {x['id']: x for x in es}
    for s in es:
        if s['status'] in ('PENDING', 'READY', 'BLOCKED') and all(
                by.get(d, {'status': 'DONE'})['status'] in ('DONE', 'SKIPPED') for d in s.get('depends_on', [])):
            return s
    return next((s for s in es if s['status'] not in ('DONE', 'SKIPPED')), None)


def progress_bar(p):
    n = max(0, min(10, round(p / 10)))
    return '●' * n + '○' * (10 - n)


def status_label(st):
    """Rótulo humano do estado (V2.3): nunca mostra 100% antes do empacotamento
    validado. Ao concluir a última etapa habilitada, mostra 'Pronto para gerar ZIP'."""
    if st['state'] == 'EMPACOTADO':
        return f"100% · Empacotado"
    if st['state'] == 'PRONTO_PARA_EMPACOTAR':
        return "Pronto para gerar ZIP"
    return f"{st['percent']}% · {st['done_count']}/{st['enabled_count']} etapas concluídas"


def nav_line(prev, nxt):
    parts = []
    if prev:
        parts.append('← ' + wikilink(prev['output'], 'Anterior'))
    parts += [wikilink('00 - COMEÇAR AQUI.md', 'Início'), wikilink('01 - PAINEL DO CICLO.md', 'Painel')]
    if nxt:
        parts.append(wikilink(nxt['output'], 'Próxima →'))
    else:
        parts.append(wikilink('99 - FINALIZAR E GERAR ZIP.md', 'Finalizar →'))
    return ' · '.join(parts)


def artefato(step, pack_id):
    return step['artefato_id'].replace('{pack_id}', pack_id or 'XXX')


def tema(st):
    return st.get('cycle_title') or st.get('pack_id') or 'este ciclo'


def gancho(step, st):
    """Pergunta de orientação personalizada pelo tema escolhido pelo usuário.
    É um gancho — ajuda a saber o que produzir — nunca uma resposta pronta:
    a área de preenchimento continua nascendo vazia."""
    g = step.get('gancho') or ''
    return g.replace('{tema}', tema(st))


def context_block(st, step, pack_id):
    """Contexto de referência RECOLHIDO: aponta para os artefatos de etapas
    anteriores (por link), nunca copia o conteúdo já preenchido para dentro
    da área de execução desta etapa."""
    by = {s['id']: s for s in st['steps']}
    refs = step.get('context_refs') or []
    lines = []
    for rid in refs:
        r = by.get(rid)
        if not r:
            continue
        marca = '✓' if r['status'] == 'DONE' else ('–' if r['status'] == 'SKIPPED' else '…')
        lines.append(f"> - {marca} **{artefato(r, pack_id)}** — {wikilink(r['output'], r.get('ui_title') or r['title'])}")
    if not lines:
        lines.append("> - (nenhuma etapa anterior referenciada)")
    return '\n'.join(lines)


def render_step_page(root, st, step, is_new):
    f = root / step['output']
    bloco_nome = BLOCO_NOME.get(step['bloco'], step['bloco'])
    pack_id = st.get('pack_id')
    if is_new or not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        text = f'''---
tipo: "Etapa editorial"
etapa_id: "{step['id']}"
bloco: "{step['bloco']} — {bloco_nome}"
estado: "{STATUS_PT.get(step['status'], step['status'])}"
cssclasses:
  - obsidian-editorial
  - editorial-hig
---
<!-- NAVEGACAO:INICIO -->
> [!navegacao]
> [PREENCHER PELA SKILL]
<!-- NAVEGACAO:FIM -->

# {step.get('ui_title') or step['title']}

> [!agora] Agora · Bloco {step['bloco']} — {bloco_nome}
> {step['objetivo']}

> [!entrega] Entregue isto — o único entregável ativo desta etapa
> **{artefato(step, pack_id)}**

> [!gancho] Para "{tema(st)}"
> {gancho(step, st)}

## Preencha aqui
<!-- PREENCHIMENTO:INICIO -->
[PREENCHER]
<!-- PREENCHIMENTO:FIM -->

## Evidência
<!-- EVIDENCIA:INICIO -->
- [PREENCHER: arquivo, link, decisão ou outra evidência verificável]
<!-- EVIDENCIA:FIM -->

<!-- PRONTO:INICIO -->
> [!pronto] Pronto quando
> - [ ] {step['dod']}
<!-- PRONTO:FIM -->

> [!contexto]- Contexto de referência (consulte; não copie para dentro do preenchimento)
{context_block(st, step, pack_id)}

<!-- NAVEGACAO-RODAPE:INICIO -->
> [!proximo] Próximo passo
> [PREENCHER PELA SKILL]
<!-- NAVEGACAO-RODAPE:FIM -->
'''
        f.write_text(text, encoding='utf-8')
    return f


def render_step_nav(root, st):
    es = enabled_steps(st)
    for i, s in enumerate(es):
        f = render_step_page(root, st, s, is_new=not (root / s['output']).exists())
        prev = es[i - 1] if i else None
        nxt = es[i + 1] if i + 1 < len(es) else None
        top = '> [!navegacao]\n> ' + nav_line(prev, nxt)
        next_target = (wikilink(nxt['output'], f"Abrir {nxt.get('ui_title') or nxt['title']} →") if nxt
                       else wikilink('99 - FINALIZAR E GERAR ZIP.md', 'Finalizar e gerar ZIP →'))
        bottom = '> [!proximo] Próximo passo — o único avanço possível a partir daqui\n> Quando esta etapa estiver concluída: **' + next_target + '**'
        text = f.read_text(encoding='utf-8')
        text = replace_block(text, 'NAVEGACAO', top) if '<!-- NAVEGACAO:INICIO -->' in text else text
        text = replace_block(text, 'NAVEGACAO-RODAPE', bottom) if '<!-- NAVEGACAO-RODAPE:INICIO -->' in text else text
        f.write_text(text, encoding='utf-8')


def render_root_pages(root):
    root = Path(root)
    st = load_json(arquivo_estado(root))
    job = load_json(arquivo_ciclo(root))
    form = job.get('form', {})
    title = form.get('cycle_title') or job.get('pack_id') or st['job_id']
    es = enabled_steps(st)
    cur = current_step(st)
    cur_link = wikilink(cur['output'], f"ABRIR AGORA · {cur.get('ui_title') or cur['title']} →") if cur else wikilink('99 - FINALIZAR E GERAR ZIP.md', 'FINALIZAR →')
    idx = es.index(cur) if cur in es else len(es) - 1
    upcoming = es[idx:idx + 3] if cur else []
    next_rows = '\n'.join(f"- {ICON.get(s['status'], '•')} **{s['id']}** ({s['bloco']}) — {wikilink(s['output'], s.get('ui_title') or s['title'])}" for s in upcoming)
    done = [s for s in es if s['status'] in ('DONE', 'SKIPPED')]
    done_rows = '\n'.join(f"> - {ICON.get(s['status'], '•')} {wikilink(s['output'], s.get('ui_title') or s['title'])}" for s in done) or '> Nenhuma ainda.'
    all_rows = '\n'.join(f"> - {ICON.get(s['status'], '•')} **{s['id']}** ({s['bloco']}) — {wikilink(s['output'], s.get('ui_title') or s['title'])} · {STATUS_PT.get(s['status'], s['status'])}" for s in es)

    decisao_callout = ''
    if pending_product_decision(st):
        decisao_callout = '''
> [!decisao] Decisão pendente
> O artigo master está concluído. Antes de continuar: **o CTA deste ciclo gera uma solução/produto?**
> Se sim, registre `produto_esperado = true` para abrir o Bloco D. Se não, registre `false` para pular direto ao Bloco E (Design & Visual). Não avance sem essa decisão explícita — ela nunca é presumida.
'''

    start = f'''---
tipo: "Entrada do ciclo"
status: "{status_label(st)}"
progresso: {st['percent']}
cssclasses:
  - obsidian-editorial
  - editorial-hig
---
# {title}

> [!agora] Agora · {status_label(st)}
> **{progress_bar(st['percent'])}**
>
> Você não precisa escolher o próximo arquivo. Continue daqui:
>
> **{cur_link}**
{decisao_callout}
> [!entrega] Como trabalhar
> 1. Abra a etapa atual.
> 2. Preencha somente o que ela pede — um único entregável por etapa.
> 3. Registre arquivo/link e evidência.
> 4. Marque o critério de pronto (um só, objetivo).
> 5. Use **Próxima →**.

## Próximos passos
{next_rows or '- Nenhum. O ciclo está pronto para finalização.'}

## Atalhos
- {wikilink('01 - PAINEL DO CICLO.md', 'Ver o painel do ciclo')}
- {wikilink('98 - CHECKLIST FINAL.md', 'Fazer checklist final')}
- {wikilink('99 - FINALIZAR E GERAR ZIP.md', 'Finalizar e gerar ZIP')}

> [!contexto]- Etapas já concluídas
{done_rows}

> [!contexto]- Ver a trilha completa (8 blocos da SOP-KP-001)
{all_rows}
'''
    (root / '00 - COMEÇAR AQUI.md').write_text(start, encoding='utf-8')

    panel = f'''---
tipo: "Painel do ciclo"
cssclasses:
  - obsidian-editorial
  - editorial-hig
---
# Painel do ciclo

> [!navegacao]
> [[00 - COMEÇAR AQUI|← Início]] · [[99 - FINALIZAR E GERAR ZIP|Finalizar →]]

> [!agora] Etapa atual · Bloco {st.get('bloco_atual') or '—'}
> **{status_label(st)}**
>
> {cur_link}
{decisao_callout}
## Próximas 3
{next_rows or '- Nenhuma pendência antes da finalização.'}

> [!contexto]- Trilha completa
{all_rows}
'''
    (root / '01 - PAINEL DO CICLO.md').write_text(panel, encoding='utf-8')

    (root / '98 - CHECKLIST FINAL.md').write_text('''---
tipo: "Checklist final"
cssclasses:
  - obsidian-editorial
  - editorial-hig
---
# Checklist final

> [!navegacao]
> [[00 - COMEÇAR AQUI|← Início]] · [[99 - FINALIZAR E GERAR ZIP|Finalizar →]]

> [!agora] Faça uma última passagem
> Marque apenas o que você realmente conferiu.

> [!pronto] Pronto para gerar o ZIP quando
> - [ ] Todas as etapas habilitadas estão concluídas ou não aplicáveis (o painel mostra "Pronto para gerar ZIP" quando isso é verdade).
> - [ ] O Bloco D (produto) tem uma decisão explícita registrada — ativado e concluído, ou explicitamente não aplicável.
> - [ ] Arquivos e links do Drive estão registrados.
> - [ ] Evidências estão preenchidas.
> - [ ] Nomes e versões estão corretos.
> - [ ] Checklist de QA & Governança (Bloco G) está aprovado.

> [!contexto]- Importante
> "Pronto para gerar ZIP" não é 100%. O ciclo só chega a **100% Empacotado** depois que o pacote é gerado e validado (hashes conferidos). O aceite real de qualquer etapa fora desta skill (ex.: publicação por terceiros) precisa de evidência própria — nunca presumir.
''', encoding='utf-8')

    (root / '99 - FINALIZAR E GERAR ZIP.md').write_text('''---
tipo: "Finalização do ciclo"
cssclasses:
  - obsidian-editorial
  - editorial-hig
---
# Finalizar e gerar ZIP

> [!navegacao]
> [[98 - CHECKLIST FINAL|← Checklist final]] · [[00 - COMEÇAR AQUI|Início]]

> [!agora] Última ação
> Confira o checklist e então peça à skill para **sincronizar, validar e gerar o ZIP**.

> [!entrega] Resultado esperado
> Um ZIP com manifesto, hashes e todos os entregáveis do ciclo — o estado do painel muda de "Pronto para gerar ZIP" para **"100% Empacotado"** somente depois que o pacote é gerado e os hashes conferidos.

## Registro do pacote
- **Arquivo ZIP:** [PREENCHER PELA SKILL]
- **SHA-256 do manifesto:** [PREENCHER PELA SKILL]
- **Estado antes de gerar:** Pronto para gerar ZIP
- **Estado depois de gerar e validar:** 100% Empacotado

> [!contexto]- Empacotado não é publicado
> "100% Empacotado" é um estado técnico deste ciclo (todas as etapas concluídas + pacote validado). Não é o mesmo que aceite de terceiros fora desta skill; qualquer aceite externo precisa de evidência própria antes de ser declarado.
''', encoding='utf-8')

    render_step_nav(root, st)


def render_all(root):
    render_root_pages(Path(root))
