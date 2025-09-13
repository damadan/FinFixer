from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from example import main


def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello" in captured.out
