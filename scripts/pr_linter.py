import sys
import re
import requests
import os

GITHUB_API_URL = "https://api.github.com"

def validate_title(title, branch_name):
    title_clean = title.lower().strip().replace("-", " ").replace("_", " ")
    branch_clean = branch_name.lower().strip().replace("-", " ").replace("_", " ")

    if title_clean == branch_clean:
        return False, "Title must not be identical to the branch name."

    if len(title.strip()) < 10:
        return False, "Title is too short. Add more context."

    if " " not in title:
        return False, "Title must contain multiple words for clarity."

    return True, None

def validate_body_structure(body):
    errors = []
    warnings = []

    sections = {
        "1. Issue": "### 1. Issue",
        "2. Description": "### 2. Description of change",
        "3. Testing": "### 3. Testing that was done",
        "4. Don’t forget": "### 4. Don’t forget",
        "5. Notes": "### 5. Additional Notes"
    }

    # Mandatory: Issue section
    if sections["1. Issue"] not in body:
        errors.append("Missing required section: `### 1. Issue`.")
    else:
        issue_block = body.split(sections["1. Issue"])[1].split("###")[0]
        closes_valid = re.search(r"Closes:\s*#\d+", issue_block)
        related_valid = re.search(r"Related:\s*#\d+", issue_block)
        if not (closes_valid or related_valid):
            errors.append("`Issue` section must include `Closes: #<number>` or `Related: #<number>`.")

    # Mandatory: Description section
    if sections["2. Description"] not in body:
        errors.append("Missing required section: `### 2. Description of change`.")
    else:
        desc_block = body.split(sections["2. Description"])[1].split("###")[0]
        desc_lines = [
            line for line in desc_block.strip().splitlines()
            if line.strip() and line.strip() not in ["•", "-", "*"]
        ]
        if len(desc_lines) < 2:
            errors.append("`Description of change` must contain at least 2 lines.")
        desc_word_count = sum(len(line.strip().split()) for line in desc_lines)
        if desc_word_count < 10:
            errors.append("Description of change must contain at least 10 meaningful words.")
            
    # Optional: Warn if soft sections are missing
    sections = ["Testing that was done", "Don’t forget", "Additional Notes"]
    for section in sections:
        if not any(section.lower() in line.lower() for line in body.splitlines()):
            warnings.append(f"Recommended section missing: {section}")

    return errors, warnings

def validate_labels(labels):
    label_names = [label["name"] for label in labels]
    required_labels = ["Risk: Low", "Risk: High"]

    if not any(risk_label in label_names for risk_label in required_labels):
        return False, "PR must be labeled with either 'Risk: Low' or 'Risk: High'."
    return True, None

def post_comment(repo, pr_number, token, message):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": message}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        print(f"⚠️ Failed to post comment. Status: {response.status_code} — {response.text}")
    else:
        print("\n💬 Comment posted successfully on the PR.")
        
def main():
    pr_number = os.environ["PR_NUMBER"]
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]

    headers = {"Authorization": f"Bearer {token}"}
    pr_url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}"
    response = requests.get(pr_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch PR info. Status code: {response.status_code}")
        sys.exit(1)

    pr_data = response.json()

    # Skip if it's still a draft
    if pr_data.get("draft", False):
        print("⚠️ Skipping validation: PR is still in draft mode.")
        sys.exit(0)
        
    title = pr_data["title"]
    body = pr_data.get("body", "")
    branch_name = pr_data["head"]["ref"]

    errors = []

    # Label Validaion
    labels = pr_data.get("labels", [])
    is_label_valid, label_error = validate_labels(labels)
    if not is_label_valid:
        errors.append(f"❌ {label_error}")

    is_title_valid, title_error = validate_title(title, branch_name)
    if not is_title_valid:
        errors.append(f"❌ {title_error}")

    body_errors, body_warnings = validate_body_structure(body)
    errors.extend(f"❌ {err}" for err in body_errors)
    
    if errors:
        full_error_message = "❌ **PR validation failed:**\n\n" + "\n".join(errors)
        if body_warnings:
            full_error_message += "\n\n⚠️ **Warnings:**\n" + "\n".join(f"- {w}" for w in body_warnings)
        print(full_error_message)
        post_comment(repo, pr_number, token, full_error_message)
        sys.exit(1)

    print("✅ PR title and description are valid.")

if __name__ == "__main__":
    main()
