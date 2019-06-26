#!/usr/bin/env python

from os import environ
from datetime import datetime, timedelta
import re
from glob import glob
import json
import yaml
from github import Github
import requests


class Gazer(object):
    def __init__(self):
        self.hub = Github(self.get_config_var("GAZER_API_TOKEN"))
        self.me = self.hub.get_user()
        self.org = self.hub.get_organization(self.get_config_var("ORG_NAME"))
        self.review_repos = [
            self.org.get_repo(repo_name)
            for repo_name in self.get_config_var("REVIEW_REPOS")
        ]
        self.release_repos = [
            self.org.get_repo(repo_name)
            for repo_name in self.get_config_var("RELEASE_REPOS")
        ]
        self.days_depth = self.since(self.get_config_var("DAYS_DEPTH"))
        self.release_regex = re.compile(self.get_config_var("RELEASE_REGEX"))
        self.slack_webhook = self.get_config_var("SLACK_WEBHOOK")

    def get_config_var(self, v):
        """Override config from env or read them from config file."""
        if environ.get(v):
            return environ.get(v)
        with open(glob("**/config/config.yaml", recursive=True)[0], "r") as stream:
            return yaml.safe_load(stream)[v]

    def since(self, days):
        """Get datetime object for days since back to look.  Set to 2 for weekend."""
        since = datetime.utcnow() - timedelta(days=days)
        return since

    def poll_my_review_requests(self):
        """Get current notifications about your review requests, and send a slack message to a specified webhook."""
        for note in self.me.get_notifications(since=self.days_depth):
            if (
                note.repository in self.review_repos
                and note.reason == "review_requested"
                and note.subject.type == "PullRequest"
                and note.unread
            ):
                pull = note.repository.get_pull(
                    int(note.subject.url.split("pulls/")[1])
                )
                payload = json.dumps(
                    {
                        "text": f"""Your review is requested in {note.repository.name}. 
                    \nSubject: {note.subject.title}
                    \n{pull.html_url}"""
                    }
                )
                # Send the Slack message, mark the notification as read.
                requests.post(self.slack_webhook, data=payload)
                note.mark_as_read()

    def poll_release_pull_requests(self):
        """Poll for pull requests to an active release branch."""
        for repo in self.release_repos:
            release_branches = [
                branch
                for branch in repo.get_branches()
                if self.release_regex.fullmatch(branch.name)
            ]
            pulls = [
                pull
                for pull in repo.get_pulls(state="open")
                if pull.head in release_branches
            ]
            for pull in pulls:
                payload = json.dumps(
                    {
                        "text": f"""A new pull request has been created for {repo_name} at {pull.head}.
                                \n{pull.html_url}"""
                    }
                )
                # Send the Slack Notification
                requests.post(self.slack_webhook, data=payload)

    def poll_and_notify_all(self):
        """Run poll and notify for both review requests, and prs against release branches."""
        self.poll_my_review_requests()
        self.poll_release_pull_requests()
