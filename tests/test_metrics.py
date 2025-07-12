from ticketsmith.metrics import start_metrics_server, REQUEST_LATENCY
import urllib.request
import time


def test_metrics_endpoint():
    start_metrics_server(8001)
    REQUEST_LATENCY.observe(0.1)
    time.sleep(0.1)
    with urllib.request.urlopen("http://localhost:8001/metrics") as resp:
        data = resp.read().decode()
    assert "ticketsmith_request_latency_seconds" in data
