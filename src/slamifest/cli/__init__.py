# SPDX-FileCopyrightText: 2024-present Harry Reeder <harry@harryreeder.co.uk>
#
# SPDX-License-Identifier: MIT
import json
from getpass import getpass

import click
import requests
from halo import Halo

# from slamifest.__about__ import __version__
from slamifest.tokens import get_token, refresh_stored_token


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
# @click.version_option(version=__version__, prog_name="slamifest") # TODO: Re-implement this now we're using hatch-vcs
@click.option(
    "-p",
    "--profile",
    default="default",
    help="Slamifest profile name, allowing multiple side by side configs",
)
@click.pass_context
def slamifest(ctx, profile):
    ctx.ensure_object(dict)
    ctx.obj["PROFILE"] = profile


@slamifest.command()
@click.pass_context
def login(ctx):
    """Set up a slamifest profile & generate tokens."""
    profile = ctx.obj["PROFILE"]

    click.echo(
        'Please navigate to the "Managing configuration tokens" section'
        " here: https://api.slack.com/reference/manifests#config-tokens"
    )
    refresh_token = getpass("Enter your workspace's refresh token: ")

    with Halo(f"Storing Token for Profile: {profile}"):
        refresh_stored_token(profile, refresh_token)


@slamifest.command()
@click.option(
    "-m",
    "--manifest",
    default="manifest.json",
    type=click.File("r"),
    help="Set the manifest file name",
)
@click.argument("APP_ID")
@click.pass_context
def upload(ctx, app_id, manifest):
    """Upload a manifest to Slack App APP_ID."""
    profile = ctx.obj["PROFILE"]
    click.echo(f"[{profile}] Uploading {manifest.name} to {app_id}\n")
    token = get_token(profile)
    manifest = json.load(manifest)

    resp = requests.post(
        "https://slack.com/api/apps.manifest.update",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={"app_id": app_id, "manifest": manifest},
        timeout=30,
    )

    for key, val in resp.json().items():
        click.echo(f"{key}: {val}")
