import json
from ticketsmith.privacy import add_processing_activity, record_dpia


def test_add_processing_activity(tmp_path):
    path = tmp_path / "register.json"
    add_processing_activity(str(path), {"id": "PR1", "activity": "test"})
    with open(path) as f:
        data = json.load(f)
    assert data[0]["activity"] == "test"


def test_record_dpia(tmp_path):
    path = tmp_path / "dpia.json"
    record_dpia(str(path), "feature", ["risk"], "mitigation")
    with open(path) as f:
        data = json.load(f)
    assert data[0]["feature"] == "feature"
    assert data[0]["risks"] == ["risk"]
