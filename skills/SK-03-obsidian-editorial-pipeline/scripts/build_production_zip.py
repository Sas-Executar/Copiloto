#!/usr/bin/env python3
from pathlib import Path
import argparse, zipfile
from common import load_json, save_json, sha256, arquivo_estado, arquivo_manifesto
from state_engine import recalc
from navegacao import render_all

ap = argparse.ArgumentParser()
ap.add_argument('job')
ap.add_argument('--out', required=True)
a = ap.parse_args()
root = Path(a.job).resolve()
render_all(root)
st = load_json(arquivo_estado(root))
recalc(st)

if st['state'] not in ('PRONTO_PARA_EMPACOTAR', 'EMPACOTADO'):
    raise SystemExit(f"Pacote bloqueado: ciclo ainda não concluiu todas as etapas habilitadas "
                      f"({st['done_count']}/{st['enabled_count']} concluídas, estado={st['state']}). "
                      f"Empacotar não é o gate — todas as etapas concluídas é o gate.")

files = [p for p in root.rglob('*') if p.is_file() and '.obsidian' not in p.parts
         and p.suffix.lower() not in ('.zip', '.skill') and '__pycache__' not in p.parts]
manifest = {'job_id': st['job_id'], 'state': st['state'], 'percent': st['percent'],
            'done': st['done_count'], 'enabled': st['enabled_count'],
            'files': [{'path': str(p.relative_to(root)), 'sha256': sha256(p), 'bytes': p.stat().st_size} for p in files]}
save_json(arquivo_manifesto(root), manifest)

# o manifesto acabou de ser escrito: reincluir na lista de arquivos do zip
files = [p for p in root.rglob('*') if p.is_file() and '.obsidian' not in p.parts
         and p.suffix.lower() not in ('.zip', '.skill') and '__pycache__' not in p.parts]
out = Path(a.out)
out.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, p.relative_to(root))

# só agora, com o zip gerado e o manifesto com hashes gravado, o ciclo pode
# ser declarado 100% Empacotado — nunca antes.
st['packaged'] = True
st['package_evidence'] = [str(out), str(arquivo_manifesto(root).relative_to(root))]
recalc(st)
save_json(arquivo_estado(root), st)
render_all(root)
print(out)
