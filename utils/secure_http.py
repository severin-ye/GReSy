from typing import Optional
from urllib.parse import urlparse
import requests


class SecureSession:
    """A small wrapper around requests.Session that defaults to safer behavior.

    - Disables trust_env by default (no automatic .netrc / env credentials).
    - Provides a get() helper that can block cross-host redirects when
      allow_redirects=True and same_host_only=True.
    """

    def __init__(self, trust_env: bool = False):
        self.session = requests.Session()
        self.session.trust_env = trust_env

    def get(self, url: str, *, allow_redirects: bool = False, timeout: int = 10, same_host_only: bool = True):
        """Perform a GET with safer defaults.

        If allow_redirects is True and same_host_only is True, any 3xx with a
        Location header that points to a different hostname will raise ValueError.
        """
        r = self.session.get(url, allow_redirects=allow_redirects, timeout=timeout)

        if allow_redirects and same_host_only and 300 <= getattr(r, "status_code", 0) < 400:
            headers = getattr(r, "headers", {}) or {}
            if 'Location' in headers:
                loc = headers['Location']
                if urlparse(loc).hostname != urlparse(url).hostname:
                    raise ValueError("Blocked cross-host redirect")

        return r


__all__ = ["SecureSession"]
