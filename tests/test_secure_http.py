import pytest
from utils.secure_http import SecureSession


class DummyResponse:
    def __init__(self, status_code=200, headers=None):
        self.status_code = status_code
        self.headers = headers or {}


def test_get_no_redirect_returns_response(monkeypatch):
    s = SecureSession()
    dummy = DummyResponse(200, {})

    def fake_get(url, allow_redirects, timeout):
        return dummy

    monkeypatch.setattr(s.session, "get", fake_get)
    resp = s.get("https://example.com", allow_redirects=False)
    assert resp is dummy


def test_block_cross_host_redirect_raises(monkeypatch):
    s = SecureSession()
    dummy = DummyResponse(302, {"Location": "https://evil.com/path"})

    def fake_get(url, allow_redirects, timeout):
        return dummy

    monkeypatch.setattr(s.session, "get", fake_get)
    with pytest.raises(ValueError):
        s.get("https://example.com", allow_redirects=True, same_host_only=True)
