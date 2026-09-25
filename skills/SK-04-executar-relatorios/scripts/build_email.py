#!/usr/bin/env python3
"""Gera os templates de e-mail HTML a partir das fontes *.email.src.html (perfil "email").

Clientes de e-mail não suportam custom properties CSS: cada var(--exec-*) da fonte é trocado pelo
valor resolvido em assets/tokens/tokens.json (mesmo resolvedor do tokens.css). A saída é o único
lugar onde hex aparece num template, e só porque foi gerada a partir dos tokens.

Uso:  build_email.py            (regrava as saídas)
      build_email.py --checar   (falha se alguma saída estiver desatualizada — usado no validate_skill)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens import Tokens  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
VAR = re.compile(r"var\(--(exec-[a-z0-9-]+)\)")
CABECALHO = "<!-- GERADO por scripts/build_email.py a partir de {fonte} + assets/tokens/tokens.json. Não editar à mão. -->\n"


def mapa_css(t: Tokens) -> dict[str, str]:
    out = {}
    for nome in t.nomes_alias():
        v = t.resolve(nome)
        if v is not None:
            out[t._nome_css(nome)] = str(v)
    return out


def construir(fonte: Path, t: Tokens) -> str:
    valores = mapa_css(t)
    texto = fonte.read_text(encoding="utf-8")

    def troca(m):
        nome = m.group(1)
        if nome not in valores:
            raise ValueError(f"{fonte.name}: token indefinido ou LACUNA: --{nome}")
        # aspas duplas de pilhas de fonte quebrariam o atributo style="..."
        return valores[nome].replace('"', "'")

    corpo = VAR.sub(troca, texto)
    corpo = re.sub(r"<!--\s*\n\s*FONTE.*?-->\n", "", corpo, count=1, flags=re.S)
    return corpo.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + CABECALHO.format(fonte=f"assets/templates/{fonte.name}"), 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checar", action="store_true")
    a = ap.parse_args()
    t = Tokens.load()
    desatualizados = 0
    for fonte in sorted(TEMPLATES.glob("*.email.src.html")):
        destino = fonte.with_name(fonte.name.replace(".email.src.html", ".email.html"))
        novo = construir(fonte, t)
        if a.checar:
            if not destino.exists() or destino.read_text(encoding="utf-8") != novo:
                print(f"DESATUALIZADO: {destino.relative_to(ROOT)} (rode scripts/build_email.py)")
                desatualizados += 1
            else:
                print(f"ok: {destino.relative_to(ROOT)}")
        else:
            destino.write_text(novo, encoding="utf-8")
            print(f"escrito: {destino.relative_to(ROOT)}")
    return 1 if desatualizados else 0


if __name__ == "__main__":
    raise SystemExit(main())
