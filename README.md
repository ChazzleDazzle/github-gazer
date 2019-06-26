# github-gazer

Watch for GitHub review requests, and release branch pull requests, and notify on Slack.

## Installation

Clone and install from local.  From root directory, run:  

```bash
pip install .
```

## Configure

Copy and edit the config file at `gazer/config/config.yaml.template`, or override those options with environment variables of the same names.

## Usage

Default usage will run a poll against your configured repos.  

```bash
gazer
```

Suggested usage would be to set up a local cron to poll regularly.

```cron
0/2 9-16 * * MON-FRI /path/to/my/virtualenv/gazer/bin/python3 gazer
```
