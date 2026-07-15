import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("numtowords", Path(__file__).with_name("numtowords.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_append_number_to_history(tmp_path):
    history_path = tmp_path / "converted_numbers.txt"

    module.append_number_to_history("123.45", str(history_path))
    module.append_number_to_history("67", str(history_path))

    contents = history_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(contents) == 2
    assert contents[0].startswith("1. 123.45 ")
    assert contents[1].startswith("2. 67 ")


def test_history_path_uses_executable_directory_for_frozen_app(monkeypatch, tmp_path):
    monkeypatch.setattr(module.sys, "frozen", True, raising=False)
    monkeypatch.setattr(module.sys, "executable", str(tmp_path / "app.exe"), raising=False)

    history_path = module.get_history_file_path()
    expected_name = f"converted_numbers_{module.datetime.now().strftime('%Y-%m-%d')}.txt"

    assert history_path == str(tmp_path / expected_name)
