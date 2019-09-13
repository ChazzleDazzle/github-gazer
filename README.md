# github-gazer

Watch for GitHub review requests, and release branch pull requests, and notify on Slack.

## Installation

Clone and install from local.  From root directory, run:  

```bash
mkvritualenv --python=`which python3` gazer && pip install .
```

## Configure

Copy and edit the config file at `gazer/config/config.yaml.template`, or override those options with environment variables of the same names.

## Usage

**You must first [configure](#Configure) the app in order to use it.**

Default usage will run a poll against your configured repos.  

```bash
gazer
```

Suggested usage would be to set up a local cron to poll regularly.

Using a virtualenv, and running as a local cron:

```cron
0/2 9-16 * * MON-FRI /path/to/my/virtualenv/gazer/bin/python /path/to/my/virtualenv/gazer/bin/gazer
```

Running as a docker container:

1. Build and tag the container:
    1. From the repo's root directory: `docker build . -t gazer:latest`
1. Add the cron in crontab:
    1. `crontab -e`
    1. To run every 2 minutes, 9-5, every weekday, add: `*/2 9-17 * * MON-FRI docker run gazer`
