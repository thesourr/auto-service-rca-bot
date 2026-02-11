#!/usr/bin/env python3
"""
Script pentru a testa commit-ul email_queue.json via GitHub API
"""

import requests
import json
import base64

# GitHub config
TOKEN = "YOUR_GITHUB_TOKEN_HERE"
OWNER = "thesourr"
REPO = "auto-service-rca-bot"
PATH = "data/email_queue.json"
BRANCH = "main"

# Email queue pentru test
test_queue = {
    "recipients": [{
        "service_id": "test-email-001",
        "email": "ionescuionut18@gmail.com",
        "name": "Test Service Auto - Email de Test"
    }],
    "is_test": True,
    "created_at": "2026-02-11T12:30:00Z"
}

def commit_email_queue():
    """Commit email queue to GitHub"""

    # Get current file SHA (if exists)
    get_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    sha = None
    try:
        response = requests.get(get_url, headers=headers)
        if response.status_code == 200:
            sha = response.json()["sha"]
            print(f"✅ Found existing file, SHA: {sha[:8]}...")
    except Exception as e:
        print(f"ℹ️  File doesn't exist yet (first commit): {e}")

    # Prepare content
    content = json.dumps(test_queue, indent=2, ensure_ascii=False)
    content_bytes = content.encode('utf-8')
    content_base64 = base64.b64encode(content_bytes).decode('utf-8')

    # Commit payload
    commit_data = {
        "message": "🧪 Test email queue - trimite la ionescuionut18@gmail.com",
        "content": content_base64,
        "branch": BRANCH
    }

    if sha:
        commit_data["sha"] = sha

    # Commit to GitHub
    put_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"
    response = requests.put(put_url, headers=headers, json=commit_data)

    if response.status_code in [200, 201]:
        print(f"✅ Email queue committed successfully!")
        print(f"📝 Commit: {response.json()['commit']['sha'][:8]}")
        print(f"🔗 URL: {response.json()['content']['html_url']}")
        return True
    else:
        print(f"❌ Failed to commit: {response.status_code}")
        print(f"Error: {response.json()}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🧪 TEST EMAIL COMMIT")
    print("="*60)
    print(f"Repository: {OWNER}/{REPO}")
    print(f"File: {PATH}")
    print(f"Recipient: ionescuionut18@gmail.com")
    print("="*60)

    success = commit_email_queue()

    if success:
        print("\n✅ SUCCESS! Email queue committed.")
        print("\n📧 Next steps:")
        print("1. Wait 30 seconds for GitHub Actions to trigger")
        print("2. Check: https://github.com/thesourr/auto-service-rca-bot/actions")
        print("3. Verify email at: ionescuionut18@gmail.com")
        print("4. Expected subject: 'Propunere Colaborare - Recuperare Costuri Reparații Auto RCA'")
    else:
        print("\n❌ FAILED to commit email queue.")
        print("Check token permissions and try again.")
