#!/usr/bin/env python3
import argparse, json
from common import load_json, arquivo_estado
from state_engine import eligible_steps, pending_product_decision

ap = argparse.ArgumentParser()
ap.add_argument('job')
a = ap.parse_args()
st = load_json(arquivo_estado(a.job))
e = eligible_steps(st)
if e:
    result = e[0]
elif pending_product_decision(st):
    result = {'status': 'DECISAO_PENDENTE',
              'mensagem': 'Registre --produto-esperado true|false (o CTA deste ciclo gera uma solução/produto?) antes de continuar.'}
else:
    result = {'status': 'SEM_ETAPA_ELEGIVEL'}
print(json.dumps(result, ensure_ascii=False, indent=2))
