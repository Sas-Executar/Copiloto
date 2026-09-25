#!/usr/bin/env python3
"""Cria um novo ciclo a partir do YAML/JSON inicial (V2.3).

Correção estrutural da V2.3: o formulário de entrada NÃO exige problem_id,
tese, evidências, artigo ou assets — esses nascem dentro da trilha, na etapa
certa (problem_id em S02, tese em S05, evidências em S12, artigo em S17...).
O único dado obrigatório aqui é o identificador do pack/ciclo. Tudo o mais
(título de trabalho, overrides de asset_plan, decisão antecipada sobre
produto_esperado) é opcional e pode ser preenchido depois, dentro da trilha.
"""
from pathlib import Path
import argparse
from common import load_json, save_json, process_spec, PASTA_SISTEMA, ARQUIVO_CICLO, ARQUIVO_ESTADO
from state_engine import recalc
from navegacao import render_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('form')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    form = load_json(a.form)
    proc = process_spec()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    pack_id = form.get('pack_id')
    if not pack_id:
        raise SystemExit('O formulário inicial precisa apenas de "pack_id" (identificador do pack/ciclo, ex.: "TP-002"). '
                          'problem_id, tese, evidências, artigo e assets nascem dentro da trilha — não aqui.')
    job_id = form.get('cycle_id') or f"JOB-{pack_id}"

    plan = dict(proc['default_assets'])
    plan.update(form.get('asset_plan') or {})

    steps = []
    for s in proc['steps']:
        enabled = True
        status = 'PENDING'
        if s.get('asset_key') and int(plan.get(s['asset_key'], 0)) == 0:
            enabled = False
            status = 'SKIPPED'
        if s.get('conditional') == 'produto':
            # decisão só é conhecida dentro da trilha (S17); nunca presumir aqui
            enabled = False
            status = 'PENDING'
        steps.append({
            **s,
            'enabled': enabled,
            'status': status,
            'outputs': [],
            'evidence': [],
        })

    state = {
        'job_id': job_id,
        'pack_id': pack_id,
        'cycle_title': form.get('cycle_title') or pack_id,
        'process_id': proc['id'],
        'wip_limit': 1,
        'produto_esperado': form.get('produto_esperado'),  # None = decidir em S17
        'packaged': False,
        'package_evidence': [],
        'handoff_accepted': False,
        'handoff_evidence': [],
        'steps': steps,
    }
    recalc(state)

    job = {'job_id': job_id, 'pack_id': pack_id, 'process_id': proc['id'], 'form': form, 'asset_plan': plan}

    for d in [PASTA_SISTEMA, '02 - TRILHA', '03 - ARQUIVOS', '04 - FONTES']:
        (out / d).mkdir(exist_ok=True)

    save_json(out / PASTA_SISTEMA / ARQUIVO_CICLO, job)
    save_json(out / PASTA_SISTEMA / ARQUIVO_ESTADO, state)

    render_all(out)
    print(out)


if __name__ == '__main__':
    main()
