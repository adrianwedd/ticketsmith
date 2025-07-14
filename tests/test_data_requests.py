import json
from ticketsmith.logging_config import configure_logging
from ticketsmith.audit import configure_audit_logging
from ticketsmith.data_requests import delete_user_data, export_user_data


def test_delete_user_data(tmp_path):
    log = tmp_path / "audit.log"
    data = tmp_path / "u.txt"
    data.write_text("secret")
    configure_logging()
    configure_audit_logging(path=str(log))
    delete_user_data("u1", str(data))
    assert not data.exists()
    with open(log) as f:
        rec = json.loads(f.read())
    assert rec["event"] == "data_deletion"
    assert rec["user"] == "u1"


def test_export_user_data(tmp_path):
    log = tmp_path / "audit.log"
    src = tmp_path / "u.txt"
    dest = tmp_path / "export" / "u.txt"
    src.write_text("info")
    configure_logging()
    configure_audit_logging(path=str(log))
    export_user_data("u2", str(src), str(dest))
    assert dest.exists()
    with open(log) as f:
        rec = json.loads(f.read())
    assert rec["event"] == "data_export"
    assert rec["user"] == "u2"
