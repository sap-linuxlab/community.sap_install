#!/usr/bin/env python

import argparse
import requests
import os
import json


def get_description(requirement_file, package, latest):
    return f"""The package {package} is outdated in {requirement_file}. The latest version is {latest}. Please update the package to the latest version.

Check the package [here](https://pypi.org/project/{package}/{latest}/) for more information.
"""


def get_title(requirement_file, package_name, current_version, latest_version):
    return f"Dependency outdated in {requirement_file}: {package_name}:{current_version} -> {latest_version}"


if __name__ == '__main__':
    # Arguments parsing
    parser = argparse.ArgumentParser(description="Open issue with the correct argument")
    parser.add_argument("package", type=str, help='The name of the package')
    parser.add_argument("version", type=str, help='The current version of the package')
    parser.add_argument("latest", type=str, help='The latest version of the package')
    args = parser.parse_args()

    # Environment variable
    repo = os.environ.get("GITHUB_REPOSITORY")
    requirement_file = str(os.environ.get("REQUIREMENT_FILE"))

    # Define the title
    issue_title = get_title(requirement_file, args.package, args.version, args.latest)

    # The double quote on the issue_title is necessary to avoid duplicate issues
    query = f"repo:{repo} type:issue in:title \"{issue_title}\""

    # Send the query
    response = requests.get("https://api.github.com/search/issues", params={"q": query})
    data = response.json()

    # There is this error that we somehow try to avoid
    # {'message': "API rate limit exceeded for 93.45.31.205. (But here's the good news: Authenticated requests get a higher rate limit. Check
    # out the documentation for more details.)", 'documentation_url': 'https://docs.github.com/rest/overview/resources-in-the-rest-api#rat
    # e-limiting'}
    if data["total_count"] > 0:
        print("There is already an issue with this title!")
    else:
        issue_description = get_description(requirement_file, args.package, args.latest)
        token = os.environ.get("GITHUB_TOKEN")
        issue = {"title": issue_title, "body": issue_description}
        headers = {"Authorization": f"token {token}"}

        response = requests.post(f"https://api.github.com/repos/{repo}/issues", headers=headers, data=json.dumps(issue))

        # Check the response
        if response.status_code == 201:
            print("Issue created successfully.")
        else:
            print(f"Failed to create issue. Status code: {response.status_code}.")
