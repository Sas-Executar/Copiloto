#!/usr/bin/env python3
import argparse
from common import load_json, save_json, arquivo_estado
from state_engine import eligible_steps, recalc
from navegacao import render_all

ap = argparse.ArgumentParser()
ap.add_argument('job')
ap.add_argument('step')
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument('--start', action='store_true')
g.add_argument('--done', action='store_true')
g.add_argument('--block', action='store_true')
ap.add_argument('--output', action='append', default=[])
ap.add_argument('--evidence', action='append', default=[])
ap.add_argument('--produto-esperado', choices=['true', 'false'], default=None,
                 help='Registra a decisão explícita (SOP Bloco C/S17): o CTA deste ciclo gera uma '
                      'solução/produto? Abre ou fecha o Bloco D. Nunca é inferido automaticamente.')
a = ap.parse_args()

p = arquivo_estado(a.job)
st = load_json(p)

if a.produto_esperado is not None:
    st['produto_esperado'] = (a.produto_esperado == 'true')
    recalc(st)  # propaga enabled/status do Bloco D imediatamente

by = {s['id']: s for s in st['steps']}
s = by.get(a.step)
if not s:
    raise SystemExit('Etapa inválida')
if not s.get('enabled'):
    if s.get('conditional') == 'produto' and st.get('produto_esperado') is None:
        raise SystemExit('Etapa do Bloco D: registre --produto-esperado true (junto com este comando) antes de iniciar')
    raise SystemExit('Etapa desabilitada (não aplicável a este ciclo)')

if a.start:
    elig = {x['id'] for x in eligible_steps(st)}
    if a.step not in elig:
        raise SystemExit('Etapa não elegível ou WIP ocupado (uma etapa em andamento por vez)')
    s['status'] = 'IN_PROGRESS'
elif a.done:
    if s['status'] != 'IN_PROGRESS':
        raise SystemExit('Somente etapa IN_PROGRESS pode virar DONE')
    s['outputs'] += a.output
    s['evidence'] += a.evidence
    if not s['outputs']:
        raise SystemExit('DONE exige --output')
    if not s['evidence']:
        raise SystemExit('DONE exige --evidence')
    s['status'] = 'DONE'
else:
    s['status'] = 'BLOCKED'

recalc(st)
save_json(p, st)
render_all(a.job)
print(f"{a.step}={s['status']} | {st['percent']}% {st['state']} (decisão produto: {st.get('produto_esperado')})")
