import json
import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

pkg = types.ModuleType("ticketsmith")
sys.modules["ticketsmith"] = pkg

spec_sec = importlib.util.spec_from_file_location(
    "ticketsmith.security", ROOT / "src" / "ticketsmith" / "security.py"
)
security = importlib.util.module_from_spec(spec_sec)
sys.modules["ticketsmith.security"] = security
assert spec_sec.loader is not None
spec_sec.loader.exec_module(security)

spec_log = importlib.util.spec_from_file_location(
    "ticketsmith.logging_config",
    ROOT / "src" / "ticketsmith" / "logging_config.py",
)
logging_config = importlib.util.module_from_spec(spec_log)
logging_config.__package__ = "ticketsmith"
sys.modules["ticketsmith.logging_config"] = logging_config
assert spec_log.loader is not None
spec_log.loader.exec_module(logging_config)

spec_audit = importlib.util.spec_from_file_location(
    "ticketsmith.audit",
    ROOT / "src" / "ticketsmith" / "audit.py",
)
audit = importlib.util.module_from_spec(spec_audit)
audit.__package__ = "ticketsmith"
sys.modules["ticketsmith.audit"] = audit
assert spec_audit.loader is not None
spec_audit.loader.exec_module(audit)


def test_audit_log_written(tmp_path):
    path = tmp_path / "audit.log"
    logging_config.configure_logging()
    audit.configure_audit_logging(path=str(path))
    audit.log_security_event("login", user="alice")
    with open(path) as f:
        data = f.read()
    record = json.loads(data)
    assert record["event"] == "login"
    assert record["user"] == "alice"
