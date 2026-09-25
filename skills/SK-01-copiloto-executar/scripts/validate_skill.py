from pathlib import Path
import json, sys

root = Path(__file__).resolve().parents[1]
errors = []

skill = root / "SKILL.md"
if not skill.exists():
    errors.append("SKILL.md ausente")
else:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("frontmatter YAML ausente")
    if "name: copiloto-executar" not in text:
        errors.append("name inválido ou ausente")
    if "description:" not in text:
        errors.append("description ausente")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md excede 500 linhas")

required_paths = [
    "references/orchestrator.md",
    "references/copiloto-007.md",
    "references/produtividade.md",
    "references/operacoes.md",
    "references/commands.md",
    "references/contracts/command-router.json",
    "references/contracts/state-contract.json",
    "references/contracts/drive-bindings.json",
]
for rel in required_paths:
    if not (root/rel).exists():
        errors.append(f"recurso obrigatório ausente: {rel}")

for p in (root/"references"/"contracts").glob("*.json"):
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"JSON inválido {p.name}: {e}")

bindings_path = root/"references"/"contracts"/"drive-bindings.json"
if bindings_path.exists():
    bindings_text = bindings_path.read_text(encoding="utf-8")
    for stale in ["00_ORQUESTRADOR","01_COPILOTO-007","02_COPILOTO-PRODUTIVIDADE",
                  "03_COPILOTO-OPERACOES","05_CONTRATOS-EXECUTAVEIS","06_IO-E-TESTES"]:
        if stale in bindings_text:
            errors.append(f"binding intermediário indevido: {stale}")

if errors:
    print("NOT_READY")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("READY")
