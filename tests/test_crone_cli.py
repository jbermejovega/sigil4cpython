import json
from sigil4py.cli import main

def test_status(capsys):
    assert main(["--status"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["verdict"] == "HOLD_QUNO"
    assert not data["safe_to_ship"]

def test_help(capsys):
    assert main([]) == 0
    assert "sigil4py-check" in capsys.readouterr().out
