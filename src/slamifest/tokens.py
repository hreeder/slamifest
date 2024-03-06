from __future__ import annotations

import datetime
from typing import Literal

import keyring
import requests


def _keyring_args(profile: str, item_type: Literal["token", "refresh", "expiry"]):
    args = ["slamifest", f"{profile}."]

    if item_type == "token":
        args[1] += "token"
    elif item_type == "refresh":
        args[1] += "refresh_token"
    elif item_type == "expiry":
        args[1] += "expiry"

    return args


def refresh_stored_token(profile: str, refresh_token: str | None = None):
    if not refresh_token:
        refresh_token = keyring.get_password(*_keyring_args(profile, "refresh"))

    tokens = requests.get(
        "https://slack.com/api/tooling.tokens.rotate",
        params={"refresh_token": refresh_token},
        timeout=30,
    ).json()

    keyring.set_password(*_keyring_args(profile, "token"), tokens["token"])
    keyring.set_password(*_keyring_args(profile, "refresh"), tokens["refresh_token"])
    keyring.set_password(*_keyring_args(profile, "expiry"), str(tokens["exp"]))


def get_token(profile: str):
    exp = int(keyring.get_password(*_keyring_args(profile, "expiry")))
    now = datetime.datetime.now(datetime.UTC).timestamp()
    if exp <= now:
        refresh_stored_token(profile)

    return keyring.get_password(*_keyring_args(profile, "token"))
