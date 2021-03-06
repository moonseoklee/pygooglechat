import requests
import json

from response import *


class GoogleChat:

    def __init__(self, webhook_url: str, timeout: int = None, raise_exception: bool = False,
                 ignore_timeout: bool = False):
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.raise_exception = raise_exception
        self.ignore_timeout = ignore_timeout

    def __str__(self):
        return f"Webhook ===> {self.webhook_url}"

    def __eq__(self, other):
        return self.webhook_url == other.webhook_url

    def _post(self, text: str, timeout: int, ignore_timeout: bool):
        _response = None

        if ignore_timeout:
            try:
                _response = requests.post(url=self.webhook_url,
                                          data=json.dumps(text),
                                          headers={
                                              'Content-Type': 'application/json; charset=UTF-8'},
                                          timeout=timeout)
            except requests.exceptions.ConnectTimeout as cto:
                pass
        else:
            _response = requests.post(url=self.webhook_url,
                                      data=json.dumps(text),
                                      headers={
                                          'Content-Type': 'application/json; charset=UTF-8'},
                                      timeout=timeout)

        return CustomResponse.parse_response(_response, raise_exception=self.raise_exception)

    def send_text(self, text: str, timeout: int = None, ignore_timeout: bool = False):
        timeout = self.timeout if self.timeout else timeout
        ignore_timeout = self.ignore_timeout if self.ignore_timeout else ignore_timeout

        return self._post(text, timeout, ignore_timeout)


g = GoogleChat(
    "https://chat.googleapis.com/v1/spaces/AAAAzDc--50/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=CoaGQUGUjg2C4wYMoXM2uKGxFlo03NdQ981sdr77vGQ%3D",
    raise_exception=False, timeout=0.01, ignore_timeout=True)
t = {"text": "a"}
print(g.send_text(t))
