# Download a simple plain-text list of JIRA issues worked on recently

# Prerequisites:
#  pip install requests dotenv
#  Create a .env file or set environment variables for JIRA_EMAIL and JIRA_TOKEN

from collections import defaultdict
from dotenv import load_dotenv
import re
import requests
import os

env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
  load_dotenv(dotenv_path=env_path)

# Jira instance details.
# Each user will need to create their own API token at https://id.atlassian.com/manage-profile/security/api-tokens
# JIRA_EMAIL and JIRA_TOKEN should be set as environment variables or in a .env file in the same directory as this script.
# The other variables are probably fine left at their default settings.
# Load environment variables from .env file if not set
JIRA_INSTANCE = os.getenv("JIRA_INSTANCE", "https://concord-consortium.atlassian.net/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")  # Your Jira login email
JIRA_TOKEN = os.getenv("JIRA_TOKEN", "")  # Your Jira API token
JIRA_FILTER_ID = os.getenv("JIRA_FILTER_ID", "10146")  # Timesheet view filter

JIRA_API_URL = f"{JIRA_INSTANCE}/rest/api/3"
AUTH = (JIRA_EMAIL, JIRA_TOKEN)

if (not JIRA_EMAIL or not JIRA_TOKEN):
  print
  print ("Please set JIRA_EMAIL and JIRA_TOKEN environment variables.")
  exit(1)

def get_filter_jql():
    """Fetch the JQL query of the custom filter."""
    filter_url = f"{JIRA_API_URL}/filter/{JIRA_FILTER_ID}"
    response = requests.get(filter_url, auth=AUTH)
    if response.status_code == 200:
        data = response.json()
        return data.get("jql")
    else:
        print(f"Error fetching filter: {response.status_code}, {response.text}")
        return None

def get_issues_from_filter():
    """Fetch issues based on the custom filter's JQL query."""
    jql = get_filter_jql()
    if not jql:
        return []

    search_url = f"{JIRA_API_URL}/search"
    params = {
        "jql": jql,
        "maxResults": 50,  # Adjust as needed
        # "fields": ["summary", "status", "labels", "issuelinks"]  # Specify fields to retrieve
    }

    response = requests.get(search_url, auth=AUTH, params=params)

    if response.status_code == 200:
        return response.json().get("issues", [])
    else:
        print(f"Error fetching issues: {response.status_code}, {response.text}")
        return []

if __name__ == "__main__":
    issues = get_issues_from_filter()
    
    if issues:
        grouped_issues = defaultdict(list)
        for issue in issues:
            # print(json.dumps(issue, indent=2))
            key = issue["key"]
            summary = issue["fields"]["summary"]
            status = issue["fields"]["status"]["name"]

            ## Look for labels that represent funding sources
            labels = issue["fields"].get("labels", [])
            funder_labels = set([label.replace("-", " ") for label in labels if re.match(r"^\d", label)])
            ## Look for linked grant "issues" too
            for link in issue["fields"].get("issuelinks", []):
              linktype = link.get("type", {}).get("name")
              if linktype == "Project Charge":
                linkedissuesummary = link.get("outwardIssue", {}).get("fields", {}).get("summary")
                if linkedissuesummary:
                  funder_labels.add(linkedissuesummary)

            if funder_labels:
              for label in funder_labels:
                grouped_issues[label].append((key, summary, status))
            else:
              grouped_issues["Untagged"].append((key, summary, status))

        if grouped_issues:
          for funder, issues in sorted(grouped_issues.items()):
              print(f"\n=== {funder} ===")
              for key, summary, status in issues:
                  print(f"{key}: {summary} ({status})")


    else:
        print("No issues found.")
