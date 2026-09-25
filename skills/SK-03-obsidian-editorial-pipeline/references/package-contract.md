# Contrato do pacote (V2.3)

O ZIP só é liberado quando o estado do ciclo é `PRONTO_PARA_EMPACOTAR` (todas as
etapas habilitadas concluídas — Bloco D incluído ou excluído por decisão explícita).
`build_production_zip.py` gera o manifesto com hashes, monta o ZIP e só então marca
`packaged = true`; a partir daí (e só a partir daí) o estado vira `EMPACOTADO` e a
interface mostra "100% Empacotado". `verify_package.py` confere os hashes do ZIP
contra o manifesto. Nenhum destes dois passos é opcional para declarar 100%.

Empacotado não é publicado: aceite real de terceiros fora desta skill (ex.: outra
equipe recebendo o handoff) é um fato separado e exige `handoff_evidence` própria.
