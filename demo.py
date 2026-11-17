import json
from pathlib import Path
from harmony import analyze
from voicing import arrange


if __name__ == "__main__":
    cases = json.loads((Path(__file__).parent / "fixtures/cases.json").read_text())
    print(json.dumps({"harmony": analyze(**cases["ordinary_harmony"]),
                      "voicing": arrange(**cases["ordinary_voicing"])}, indent=2))
