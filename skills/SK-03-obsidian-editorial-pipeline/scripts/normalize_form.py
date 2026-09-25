#!/usr/bin/env python3
"""Normaliza o YAML/JSON/CSV/XLSX inicial do ciclo para o schema mínimo da V2.3.

Importante: este formulário inicial NÃO carrega problem_id, tese, evidências,
artigo ou assets — esses nascem dentro da trilha (ver SOP-KP-001, Seção 6).
Só pack_id é obrigatório; o resto é opcional e serve apenas para registrar o
que já é conhecido no momento da criação do ciclo (título de trabalho,
overrides de quantidade de asset, ou uma decisão antecipada sobre produto).
"""
from pathlib import Path
import argparse, csv, json
from common import save_json


def read_any(path):
    p = Path(path)
    ext = p.suffix.lower()
    if ext == '.json':
        return json.loads(p.read_text(encoding='utf-8'))
    if ext in ('.yaml', '.yml'):
        try:
            import yaml
        except ImportError:
            raise SystemExit('PyYAML não disponível; converta YAML para JSON.')
        return yaml.safe_load(p.read_text(encoding='utf-8'))
    if ext == '.csv':
        rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
        if not rows:
            raise SystemExit('CSV vazio')
        return rows[0]
    if ext == '.xlsx':
        try:
            import openpyxl
        except ImportError:
            raise SystemExit('openpyxl não disponível; exporte a linha para CSV/JSON.')
        wb = openpyxl.load_workbook(p, data_only=True, read_only=True)
        for ws in wb.worksheets:
            vals = list(ws.iter_rows(values_only=True))
            for i, row in enumerate(vals[:20]):
                hdr = [str(x).strip() if x is not None else '' for x in row]
                if 'pack_id' in hdr:
                    for data in vals[i + 1:]:
                        rec = {hdr[k]: data[k] for k in range(min(len(hdr), len(data))) if hdr[k]}
                        if rec.get('pack_id'):
                            return rec
        raise SystemExit('Nenhuma linha com pack_id encontrada no XLSX')
    raise SystemExit(f'Formato não suportado: {ext}')


def normalize(d):
    known = ['pack_id', 'cycle_id', 'cycle_title', 'produto_esperado']
    out = {k: d.get(k) for k in known if d.get(k) not in (None, '')}
    if isinstance(d.get('asset_plan'), dict):
        out['asset_plan'] = d['asset_plan']
    used = set(known + ['asset_plan'])
    extensions = {k: v for k, v in d.items() if k not in used and v not in (None, '')}
    if extensions:
        out['extensions'] = extensions
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('form')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = normalize(read_any(a.form))
    if not out.get('pack_id'):
        raise SystemExit('Falta pack_id — é o único campo obrigatório na entrada da V2.3. '
                          'problem_id, tese, evidências, artigo e assets nascem dentro da trilha.')
    save_json(a.out, out)
    print(a.out)


if __name__ == '__main__':
    main()
