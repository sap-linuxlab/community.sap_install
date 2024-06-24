#!/usr/bin/env python

import os
import re
import subprocess
import requests
import json

TOKEN = str(os.environ.get("GITHUB_TOKEN"))
REPOSITORY = str(os.environ.get("GITHUB_REPOSITORY"))
COMMIT_SHA = str(os.environ.get("GITHUB_SHA"))
REQUIREMENT_FILE = str(os.environ.get("REQUIREMENT_FILE"))
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}
OPEN_PR = os.environ.get("OPEN_PR")
OPEN_PR_BASE = os.environ.get("OPEN_PR_BASE")
BRANCH = "automation/dependencies_update"


def __build_packages_dict_from_file():
    print("INFO: create dictionary from file")
    packages = {}
    with open(REQUIREMENT_FILE, 'r') as file:
        lines = file.readlines()
        for line in lines:
            regex_pattern = re.compile(
                r"([a-zA-Z0-9-]+)==([0-9]+\.[0-9]+\.[0-9]+)")
            matches = regex_pattern.findall(line)
            if len(matches) > 0:
                package_name = str(matches[0][0])
                package_version = str(matches[0][1])
                packages[package_name] = package_version
    return packages


def __build_packages_dict_from_output(output):
    print("INFO: create dictionary from output")
    packages = {}
    lines = output.splitlines(output)
    for line in lines:
        regex_pattern = re.compile(
            r"([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+)")
        matches = regex_pattern.findall(line)
        if len(matches) > 0:
            package_name = str(matches[0][0])
            package_version = str(matches[0][2])
            packages[package_name] = package_version
    return packages


def __create_branch(branch, branch_data):
    response = requests.post(
        f"https://api.github.com/repos/{REPOSITORY}/git/refs",
        headers=HEADERS,
        data=json.dumps(branch_data))
    if response.status_code == 201:
        print(f"INFO: Branch created -> https://github.com/{REPOSITORY}/tree/{branch}")
    else:
        print(f"ERROR: Failed to create branch. Status code: {response.status_code}.")


def __search_issues(query):
    response = requests.get(
        "https://api.github.com/search/issues", params={"q": query})
    return response.json()['items']


def __create_issue(issue_data):
    response = requests.post(
        f"https://api.github.com/repos/{REPOSITORY}/issues",
        headers=HEADERS,
        data=json.dumps(issue_data))
    if response.status_code == 201:
        issue_number = response.json()['number']
        print(f"INFO: Issue created -> https://github.com/{REPOSITORY}/issues/{issue_number}")
        return issue_number
    else:
        print(f"ERROR: Failed to create issue. Status code: {response.status_code}.")
        return -1


def __update_issue(issue_number, issue):
    response = requests.patch(
        f"https://api.github.com/repos/{REPOSITORY}/issues/{issue_number}",
        headers=HEADERS,
        data=json.dumps(issue))
    if response.status_code == 200:
        print(f"INFO: Issue updated -> https://github.com/{REPOSITORY}/issues/{issue_number}")
    else:
        print(f"ERROR: Failed to update the issue. Status code: {response.status_code}.")


def __comment_issue(issue_number, comment):
    comment_data = {
        "body": comment
    }
    response = requests.post(
        f"https://api.github.com/repos/{REPOSITORY}/issues/{issue_number}/comments",
        headers=HEADERS,
        data=json.dumps(comment_data))
    if response.status_code == 201:
        print(f"INFO: Comment done in -> https://github.com/{REPOSITORY}/issues/{issue_number}")
    else:
        print(f"ERROR: Failed to create comment. Status code: {response.status_code}.")


def __create_pull_request(pr_data):
    response = requests.post(
        f"https://api.github.com/repos/{REPOSITORY}/pulls",
        headers=HEADERS,
        data=json.dumps(pr_data))
    if response.status_code == 201:
        pr_number = response.json()['number']
        print(f"INFO: Pull Request open -> https://github.com/{REPOSITORY}/pull/{pr_number}")
        return pr_number
    else:
        print(f"ERROR: Failed to create pull request. Status code: {response.status_code}.")
        return -1


def manage_pull_request(branch, packages_issue):
    body = f"Bumps packages in {REQUIREMENT_FILE}."
    for package in packages_issue:
        body += f"\nCloses #{packages_issue[package]}"
    title = f"Automation: number outdated packages in {REQUIREMENT_FILE}"
    pr_data = {
        "title": title,
        "body": body,
        "head": branch,
        "base": OPEN_PR_BASE
    }
    query = f"{title} repo:{REPOSITORY} is:pr in:title state:open"
    items = __search_issues(query)
    if not any(items):
        __create_pull_request(pr_data)
    elif len(items) == 1:
        pr_number = items[0]['number']
        response = requests.patch(
            f"https://api.github.com/repos/{REPOSITORY}/pulls/{pr_number}",
            headers=HEADERS,
            data=json.dumps(pr_data))
        if response.status_code == 200:
            print(f"INFO: Pull Request updated -> https://github.com/{REPOSITORY}/pull/{pr_number}")
        else:
            print(f"ERROR: Failed to update the pull requests. Status code: {response.status_code}.")
    else:
        print("ERROR: More than 1 pull-request with the same title are found! I can't update.")


def update_branch_with_changes(branch, file_to_change):
    os.system(f"""
git config --global --add safe.directory /github/workspace
git config --global user.email "dependencybot@linuxlab"
git config --global user.name "DependencyBot"
git fetch --prune
git stash push
git checkout -b {branch} origin/{branch}
git stash pop
git checkout --theirs {REQUIREMENT_FILE}
git add {file_to_change}
git commit --message=\"Update {file_to_change} on `date`\"
git push
    """)


def find_replace_in_file(file_path, find_str, replace_str):
    with open(file_path, 'r') as file:
        content = file.read()
    content = re.sub(find_str, replace_str, content)
    with open(file_path, 'w') as file:
        file.write(content)


def create_branch_if_not_exists(branch, commit_sha):
    response = requests.get(f"https://api.github.com/repos/{REPOSITORY}/branches/{branch}")
    if response.status_code == 404:
        branch_data = {"ref": "refs/heads/" + branch, "sha": commit_sha}
        __create_branch(branch, branch_data)
    else:
        print(f"INFO: Branch -> https://github.com/{REPOSITORY}/tree/{branch}")


def open_issue_for_package(package, current_version, latest_version):
    issue_title = f"Dependency outdated in {REQUIREMENT_FILE}: {package}=={current_version}"
    query = f"{issue_title} repo:{REPOSITORY} is:issue in:title state:open"
    items = __search_issues(query)
    issue_title = f"Dependency outdated in {REQUIREMENT_FILE}: {package}=={current_version} -> {latest_version}"
    issue_description = f"""
The package {package} is outdated in {REQUIREMENT_FILE}.

The latest version is {latest_version}. Please update the package to the latest version.

Check the package [here](https://pypi.org/project/{package}/{latest_version}/) for more information.
    """
    issue = {"title": issue_title,
             "body": issue_description,
             "labels": ["automation"]}
    if not any(items):
        return __create_issue(issue)
    elif len(items) == 1:
        issue_number = items[0]['number']
        old_title = items[0]['title']
        if old_title == issue_title:
            print(f"INFO: Issue -> https://github.com/{REPOSITORY}/issues/{issue_number}")
            return issue_number
        else:
            old_description = items[0]['body']
            comment = f"""
A new version of the package is out.

**Title and description is going to be updated with the latest one.**

**This is the previous title and description of this issue:**
```
Title: {old_title}
Description:
{old_description}
```
            """
            __comment_issue(issue_number, comment)
            __update_issue(issue_number, issue)
            return issue_number
    else:
        print("ERROR: More than 1 issues with the same title are found! I can't update.")
        return -1


if __name__ == '__main__':
    print("##### Collect data #####")
    os.system(f"pip3 install -r {REQUIREMENT_FILE}")
    raw_output_outdated = subprocess.run(
        ['pip3', 'list', '--outdated'],
        stdout=subprocess.PIPE,
        check=False)
    current_packages = __build_packages_dict_from_file()
    latest_packages = __build_packages_dict_from_output(raw_output_outdated.stdout.decode('utf-8'))
    print("##### Create data #####")
    packages_issue = {}
    if OPEN_PR == "True":
        create_branch_if_not_exists(BRANCH, COMMIT_SHA)
    print("##### Run checks #####")
    for package in current_packages.keys():
        print(f"----- Check {package} -----")
        if package in latest_packages:
            current_version = current_packages[package]
            latest_version = latest_packages[package]
            print(f"INFO: current version {current_version}")
            print(f"INFO: latest version {latest_version}")
            packages_issue[package] = open_issue_for_package(
                package,
                current_version,
                latest_version)

            if OPEN_PR == "True":
                line_current = package + r"==[0-9]+\.[0-9]+\.[0-9]+"
                line_latest = f"{package}=={latest_version}"
                find_replace_in_file(REQUIREMENT_FILE,
                                     line_current,
                                     line_latest)
            print("----------------")
        else:
            print(f"INFO: Skipping {package} => not in scope of {REQUIREMENT_FILE}")
            print("----------------")
    if OPEN_PR == "True":
        update_branch_with_changes(BRANCH, REQUIREMENT_FILE)
        manage_pull_request(BRANCH, packages_issue)
