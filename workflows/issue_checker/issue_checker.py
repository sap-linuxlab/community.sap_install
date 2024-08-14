#!/usr/bin/env python

import os
import sys
import requests
import re
import json

TOKEN = str(os.environ.get("GITHUB_TOKEN"))
REPOSITORY = str(os.environ.get("GITHUB_REPOSITORY"))
ISSUE_NUMBER = str(os.environ.get("GITHUB_ISSUE_NUMBER"))
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

ISSUE_STANDARD_TITLE = r'^\[Bug|Feature\](?: [\w\s]+)?(?: on [\w\s]+)?: .+$'
ISSUE_ROLE_BODY = r'### Role\s+([\w_]+)'
ISSUE_OS_BODY = r'### OS Family\s+([\w_]+)'

COMMENT_FOLLOW_STANDARD = """
Hi,

The standard for the issue title should be like this: `[Bug|Feature]: <short_description>`. Please update the issue title to follow this standard.

Example:
`[Bug]: pacemaker stop working on sles15`

Thanks
"""
COMMENT_TITLE_NOT_ALIGNED = """
Hi,

It seems that the title and the labels are not aligned. Check if the label `bug` is selected if the issue is a Bug and the label `enhancement` is selected if is a Feature.

Thanks
"""
COMMENT_MISS_SHORT_DESCRIPTION = """
Hi,

It seems that the title miss a short description.

Could you please update the tile by adding something after the issue specification?

Example:
`[Bug]: pacemaker stop working on sles15`

Thanks
"""


def get_issue_descriptor():
    response = requests.get(
        f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}",
        headers=HEADERS)
    if response.status_code == 200:
        print(f"INFO: Issue found -> https://github.com/{REPOSITORY}/issues/{ISSUE_NUMBER}")
        return response.json()
    else:
        print(f"ERROR: Failed to update the issue. Status code: {response.status_code}.")
        return {}


def is_a_feature(labels):
    for label in labels:
        if label['name'] == 'enhancement':
            return True
    return False


def is_a_bug(labels):
    for label in labels:
        if label['name'] == 'bug':
            return True
    return False


def is_title_standardise(title):
    regex_pattern = re.compile(ISSUE_STANDARD_TITLE)
    matches = regex_pattern.findall(title)

    return False if not matches else True


def post_comment_on_issue(body):
    comment_data = {
        "body": body
    }
    response = requests.post(
        f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}/comments",
        headers=HEADERS,
        data=json.dumps(comment_data))
    if response.status_code == 201:
        print(f"INFO: Comment done in -> https://github.com/{REPOSITORY}/issues/{ISSUE_NUMBER}")
    else:
        print(f"ERROR: Failed to create comment. Status code: {response.status_code}.")


def update_title_on_issue(title):
    title_data = {
        "title": title
    }
    response = requests.post(
        f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}",
        headers=HEADERS,
        data=json.dumps(title_data))
    if response.status_code == 200:
        print(f"INFO: Title updated -> https://github.com/{REPOSITORY}/issues/{ISSUE_NUMBER}")
    else:
        print(f"ERROR: Failed to update title. Status code: {response.status_code}.")


def title_composer(issue_descriptor):
    role_body = re.search(ISSUE_ROLE_BODY, issue_descriptor['body'])
    os_body = re.search(ISSUE_OS_BODY, issue_descriptor['body'])
    title_body = str.split(issue_descriptor['title'], ':')

    object_title = ""
    description_title = ""
    if title_body:
        object_title = "" + str.split(title_body[0], ' ')[0]
        description_title = "" + title_body[1]

    role_selected = ""
    if role_body:
        role_selected = " " + role_body.group(1)

    os_selected = ""
    if os_body:
        os_selected = " on " + os_body.group(1)

    return object_title + role_selected + os_selected + ":" + description_title


def is_short_description_filled(title):
    return True if str.split(title, ':')[-1].strip(" ") else False

if __name__ == '__main__':
    issue_descriptor = get_issue_descriptor()
    if issue_descriptor:
        if not is_title_standardise(issue_descriptor['title']):
            post_comment_on_issue(COMMENT_FOLLOW_STANDARD)
            sys.exit(1)

        is_bug_not_bug = "Bug" in issue_descriptor['title'] and not is_a_bug(issue_descriptor['labels'])
        is_feat_not_feat = "Feature" in issue_descriptor['title'] and not is_a_feature(issue_descriptor['labels'])
        if is_bug_not_bug or is_feat_not_feat:
            post_comment_on_issue(COMMENT_TITLE_NOT_ALIGNED)
            sys.exit(1)

        if not is_short_description_filled(issue_descriptor['title']):
            post_comment_on_issue(COMMENT_MISS_SHORT_DESCRIPTION)
            sys.exit(1)

        title = title_composer(issue_descriptor)
        if title != issue_descriptor['title']:
            update_title_on_issue(title)
