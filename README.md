# slamifest

[![PyPI - Version](https://img.shields.io/pypi/v/slamifest.svg)](https://pypi.org/project/slamifest)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slamifest.svg)](https://pypi.org/project/slamifest)

-----

`slamifest` is a command line tool to help work with Slack App Manifests.


**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

It is recommended to install `slamifest` with [pipx](https://github.com/pypa/pipx)

```console
pipx install slamifest
```

## Usage

To generate initial tokens, run `slamifest login` and follow the instructions.

```
❯ slamifest login
Please navigate to the "Managing configuration tokens" section here: https://api.slack.com/reference/manifests#config-tokens
Enter your workspace's refresh token:
```

This will use the refresh token to get a fresh access token, and store both in the [relevant system keyring](https://pypi.org/project/keyring/).

Now upload a manifest to Slack with `slamifest upload`:

```
❯ slamifest upload A1234ABCDEF
[default] Uploading manifest.json to A1234ABCDEF

ok: True
app_id: A1234ABCDEF
permissions_updated: False
```

* `-m/--manifest` can be specified to override the default `manifest.json` filename, ie `slamifest upload A1234ABCDEF -m slack_manifest.json`

### Global Options
* `-p/--profile` can be specified immediately after `slamifest` to influence which profile is in use. This allows for multiple development workstations to be available.

## License

`slamifest` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
