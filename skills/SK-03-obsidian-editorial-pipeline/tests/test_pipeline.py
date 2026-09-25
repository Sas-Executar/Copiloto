import tempfile, subprocess, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(*args, ok=True):
    r = subprocess.run([PY, *map(str, args)], capture_output=True, text=True)
    if ok and r.returncode:
        raise AssertionError(r.stdout + r.stderr)
    return r


def create(td):
    job = td / 'job'
    run(ROOT / 'scripts/create_job.py', ROOT / 'examples/editorial-form.example.json', '--out', job)
    return job


def test_create_entrypoint_navigation_validate():
    with tempfile.TemporaryDirectory() as td:
        job = create(Path(td))
        assert (job / '00 - COMEÇAR AQUI.md').exists()
        assert (job / '01 - PAINEL DO CICLO.md').exists()
        assert (job / '99 - FINALIZAR E GERAR ZIP.md').exists()
        s1 = job / '02 - TRILHA/Etapa 01 - Definir a transformação.md'
        assert s1.exists(), list((job / '02 - TRILHA').glob('*'))
        t = s1.read_text(encoding='utf-8')
        assert '[[00 - COMEÇAR AQUI|' in t and 'Próxima' in t
        assert '[PREENCHER]' in t  # área de preenchimento nasce vazia
        r = run(ROOT / 'scripts/next_action.py', job)
        assert 'S01' in r.stdout
        r = run(ROOT / 'scripts/validate_job.py', job)
        assert '"valid": true' in r.stdout


def test_no_problem_id_required_at_creation():
    # form mínimo: só pack_id
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        minimal = td / 'minimal.json'
        minimal.write_text(json.dumps({'pack_id': 'TP-MIN'}), encoding='utf-8')
        job = td / 'job'
        run(ROOT / 'scripts/create_job.py', minimal, '--out', job)
        assert (job / '00 - COMEÇAR AQUI.md').exists()


def test_wip_and_done_requires_evidence_and_single_advance():
    with tempfile.TemporaryDirectory() as td:
        job = create(Path(td))
        run(ROOT / 'scripts/update_step.py', job, 'S01', '--start')
        r = run(ROOT / 'scripts/update_step.py', job, 'S02', '--start', ok=False)
        assert r.returncode != 0
        out = '02 - TRILHA/Etapa 01 - Definir a transformação.md'
        r = run(ROOT / 'scripts/update_step.py', job, 'S01', '--done', '--output', out, ok=False)
        assert r.returncode != 0
        run(ROOT / 'scripts/update_step.py', job, 'S01', '--done', '--output', out, '--evidence', 'registro de teste')
        r = run(ROOT / 'scripts/next_action.py', job)
        assert 'S02' in r.stdout


def test_bloco_d_gated_by_explicit_decision():
    with tempfile.TemporaryDirectory() as td:
        job = create(Path(td))
        by = 'S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16'.split()
        for sid in by:
            out = _output_for(job, sid)
            run(ROOT / 'scripts/update_step.py', job, sid, '--start')
            run(ROOT / 'scripts/update_step.py', job, sid, '--done', '--output', out, '--evidence', f'evidencia {sid}')
        # S18 (Bloco D) não pode iniciar sem decisão
        r = run(ROOT / 'scripts/update_step.py', job, 'S18', '--start', ok=False)
        assert r.returncode != 0
        # fecha S17 registrando produto_esperado=false
        out17 = _output_for(job, 'S17')
        run(ROOT / 'scripts/update_step.py', job, 'S17', '--start')
        run(ROOT / 'scripts/update_step.py', job, 'S17', '--done', '--output', out17, '--evidence', 'artigo aprovado', '--produto-esperado', 'false')
        st = json.loads((job / '00-Sistema/estado-do-ciclo.json').read_text(encoding='utf-8'))
        by_id = {s['id']: s for s in st['steps']}
        assert by_id['S18']['status'] == 'SKIPPED'
        assert by_id['S18']['enabled'] is False
        # Bloco E deve estar elegível mesmo com Bloco D fechado (nunca trava o eixo principal)
        r = run(ROOT / 'scripts/next_action.py', job)
        assert 'S25' in r.stdout


def _output_for(job, sid):
    st = json.loads((job / '00-Sistema/estado-do-ciclo.json').read_text(encoding='utf-8'))
    by = {s['id']: s for s in st['steps']}
    return by[sid]['output']


def test_manual_sync():
    with tempfile.TemporaryDirectory() as td:
        job = create(Path(td))
        f = job / '02 - TRILHA/Etapa 01 - Definir a transformação.md'
        t = f.read_text(encoding='utf-8')
        t = t.replace('- [PREENCHER: arquivo, link, decisão ou outra evidência verificável]', '- transformação aprovada em briefing')
        t = t.replace('- [ ]', '- [x]', 1)
        f.write_text(t, encoding='utf-8')
        r = run(ROOT / 'scripts/sincronizar_obsidian.py', job)
        assert 'S01' in r.stdout


def test_package_blocked_until_all_enabled_done():
    with tempfile.TemporaryDirectory() as td:
        job = create(Path(td))
        r = run(ROOT / 'scripts/build_production_zip.py', job, '--out', Path(td) / 'x.zip', ok=False)
        assert r.returncode != 0


def test_progress_is_continuous_not_quantized():
    with tempfile.TemporaryDirectory() as td:
        job = create(Path(td))
        st = json.loads((job / '00-Sistema/estado-do-ciclo.json').read_text(encoding='utf-8'))
        assert st['state'] == 'PLANEJANDO'
        assert st['percent'] == 0
        out = _output_for(job, 'S01')
        run(ROOT / 'scripts/update_step.py', job, 'S01', '--start')
        run(ROOT / 'scripts/update_step.py', job, 'S01', '--done', '--output', out, '--evidence', 'ev')
        st = json.loads((job / '00-Sistema/estado-do-ciclo.json').read_text(encoding='utf-8'))
        assert st['state'] == 'EM_ANDAMENTO'
        # percentual real (1 de N habilitadas), não um degrau fixo tipo 33
        assert 0 < st['percent'] < 33
