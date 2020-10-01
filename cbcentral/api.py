"""Server API access."""

import posixpath
from collections import deque

import requests
from requests.exceptions import ConnectionError, Timeout


class CBCentralAPIError(Exception):
    """API access error."""


class CBCentralAPITimeout(CBCentralAPIError):
    """Timeout."""


class ChainballCentralAPI:
    """Central API."""

    def __init__(self, cbserver_addr, cbserver_key=None):
        """Initialize."""
        super().__init__()
        self._outgoing_queue = deque()
        self._address = cbserver_addr
        self._key = cbserver_key if cbserver_key is not None else ""

    @property
    def server_address(self):
        """Get server address."""
        return self._address

    def process_queue(self, single=False):
        """Process outgoing queue."""
        while True:
            try:
                data, sub_api, path, retry = self._outgoing_queue.popleft()
                result = self._central_api_post(
                    data=data, sub_api=sub_api, path=path
                )
                if "status" not in result or result["status"] != "ok":
                    raise CBCentralAPIError()
            except IndexError:
                break
            except (CBCentralAPITimeout, CBCentralAPIError):
                # retry
                if retry:
                    self._outgoing_queue.appendleft(
                        (data, sub_api, path, True)
                    )
            if single:
                break

    def central_api_get(self, sub_api=None, path=None, timeout=10):
        """Make a GET request."""

        # do not use access token for now
        # build request
        get_url = self._address
        if sub_api is not None:
            get_url = posixpath.join(get_url, sub_api)

        if path is not None:
            get_url = posixpath.join(get_url, path)

        # perform request (blocking)
        try:
            result = requests.get(
                get_url,
                timeout=timeout,
                headers={"Authorization": f"Api-Key {self._key}"},
            )
        except Timeout:
            raise CBCentralAPITimeout("GET timed out.")
        except ConnectionError:
            raise CBCentralAPIError("GET failed")
        if result.status_code != 200:
            raise CBCentralAPIError(
                "error querying central API: error {}".format(
                    result.status_code
                )
            )
        return result.json()

    def push_post_request(self, data, sub_api=None, path=None, retry=True):
        """Push post request into queue."""
        self._outgoing_queue.append((data, sub_api, path, retry))

    def _central_api_post(self, data, sub_api=None, path=None, timeout=10):
        """Make a POST request."""
        get_url = self._address
        if sub_api is not None:
            get_url = posixpath.join(get_url, sub_api)

        if path is not None:
            get_url = posixpath.join(get_url, path)

        try:
            result = requests.post(
                get_url,
                timeout=timeout,
                headers={"Authorization": f"Api-Key {self._key}"},
                data=data,
            )
        except Timeout:
            raise CBCentralAPITimeout("POST timed out")
        except ConnectionError:
            raise CBCentralAPIError("POST failed")

        if result.status_code != 200:
            raise CBCentralAPIError(
                "error while doing POST: error {}".format(result.status_code)
            )

        return result.json()

    def central_server_alive(self, timeout=1):
        """Check if server is alive."""
        try:
            requests.get(self._addr, timeout=timeout)
        except (Timeout, ConnectionError):
            return False

        return True
