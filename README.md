# Developer Scripts

This collection of scripts is designed to help developers automate common tasks and improve their workflow.

## Prerequisites

Python 3 is assumed.

## Installation

Clone this repository and `cd` into its directory.

Recommended:  create a [virtual environment](https://docs.python.org/3/library/venv.html) for python:

```shell
python3 -m venv venv
source venv/bin/activate
```

The first line is one-time setup; the second "source" command must be repeated each time you open a new terminal window. You should see "venv" in your prompt when the virtual environment is activated.

Install the required Python packages:

```shell
pip install -r requirements.txt
```

Create a [JIRA API token](https://id.atlassian.com/manage-profile/security/api-tokens) and put it, along
with your email address, in a `.env` file in the `src` directory (or set these environment variables):

```shell
JIRA_EMAIL = "me@concord.org" 
JIRA_TOKEN = "..."
```

## Scripts included

### `jira-tasks.py`

Prints out a simple plain-text list of JIRA tasks you've recently contributed to,
sorted by billing project.

This is intended to be useful for timesheet preparation. It shows tasks where you are the assignee, reviewer, or collaborator
that have been touched in the last 15 days.

## License

This project is licensed under the MIT License.
