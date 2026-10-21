import pytest

from devcrew import __version__, cli


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_idea_is_required():
    with pytest.raises(SystemExit) as exc:
        cli.main([])
    assert exc.value.code == 2


@pytest.mark.parametrize("idea", ["", "   ", "\t \r\n", "\u00a0\u2003"])
@pytest.mark.parametrize("has_api_key", [True, False])
def test_blank_idea_is_rejected_before_running(idea, has_api_key, monkeypatch, tmp_path, capsys):
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr("devcrew.crew.run", fake_run)
    monkeypatch.setattr(cli, "load_dotenv", lambda: None)
    monkeypatch.chdir(tmp_path)
    if not has_api_key:
        monkeypatch.delenv("OPENAI_API_KEY")

    with pytest.raises(SystemExit) as exc:
        cli.main([idea])

    assert exc.value.code == 2
    assert "idea must not be empty or whitespace-only" in capsys.readouterr().err
    assert calls == []
    assert not (tmp_path / "output").exists()


def test_missing_api_key_exits_with_hint(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY")
    monkeypatch.setattr(cli, "load_dotenv", lambda: None)
    with pytest.raises(SystemExit) as exc:
        cli.main(["a todo app"])
    assert "OPENAI_API_KEY" in str(exc.value.code)


@pytest.mark.parametrize("bad", ["/tmp/out", "../out", "~/out"])
def test_output_dir_must_be_relative(bad):
    with pytest.raises(SystemExit) as exc:
        cli.main(["a todo app", "-o", bad])
    assert exc.value.code == 2


@pytest.mark.parametrize("idea", ["a todo app", "  a todo app  "])
def test_runs_pipeline_with_options(idea, monkeypatch, tmp_path):
    calls = {}

    def fake_run(idea, output_dir, model):
        calls.update(idea=idea, output_dir=output_dir, model=model)
        return "ok"

    monkeypatch.setattr("devcrew.crew.run", fake_run)
    monkeypatch.chdir(tmp_path)
    assert cli.main([idea, "-o", "runs/todo", "-m", "gpt-4o"]) == 0
    assert calls == {"idea": idea, "output_dir": "runs/todo", "model": "gpt-4o"}
    assert (tmp_path / "runs" / "todo").is_dir()
