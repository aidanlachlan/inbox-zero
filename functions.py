# functions
from pathlib import Path
import json

INBOX = Path("inbox")

# 1. Scan the inbox
def list_emails():
    lines = []
    
    for path in sorted(INBOX.glob("*.json")):
        email = json.loads(path.read_text())
        lines.append(f"{email['id']} | {email['from']} | {email['subject']} | {email['folder']}")
        # print(path, email)
    
    return "\n".join(lines)

print(list_emails())

# 2. Open an email
def read_email(email_id):
    path = INBOX / f"{email_id}.json"
    email = json.loads(path.read_text())
    
    return(
        f"From: {email['from']}\n"
        f"Subject: {email['subject']}\n"
        f"Date: {email['date']}\n"
        f"Folder: {email['folder']}\n"
        f"\n{email['body']}\n"
    )   

# print(read_email("e006"))

# 3. Store email in a folder
def move_to_folder(email_id, folder):
    path = INBOX / f"{email_id}.json"
    email = json.loads(path.read_text())
    
    email['folder'] = folder
    path.write_text(json.dumps(email, indent=2))
    
    return f"Moved {email_id} to {folder}"
    
# move_to_folder("e002", "spammy")
# move_to_folder("e003", "spam")

# 4. Check what folders I have
def get_folders():
    folders = set()
    
    for path in sorted(INBOX.glob("*.json")):
        email = json.loads(path.read_text())
        folders.add(email['folder'])
    
    return "\n".join(sorted(folders))

print(get_folders())

# 5. Write a reply
def draft_reply(email_id, body):
    path = INBOX / f"{email_id}.json"
    email = json.loads(path.read_text())
    
    draft = (
        f"To: {email['from']}\n"
        f"Subject: Re: {email['subject']}\n"
        f"\n{body}\n"
    )

    Path("drafts").mkdir(exist_ok=True)
    Path(f"drafts/reply_to_{email_id}.txt").write_text(draft)
    return f"Draft saved for {email_id}. Nothing has been sent yet."


# 6. Flag email for human review
def flag_for_review(email_id, reason):
    flagged = Path("flagged.md")
    if flagged.exists() and f"- {email_id}:" in flagged.read_text():
        return f"{email_id} is already flagged. Nothing to do."

    with open(flagged, "a") as f:
        f.write(f"- {email_id}: {reason}\n")
    return f"Flagged {email_id} for human review."

# flag_for_review("e004", "Angry customer complaint")
# flag_for_review("e007", "weird")

# Define functions AI agent can call
FUNCTIONS = {
    "list_emails": list_emails,
    "read_email": read_email,
    "move_to_folder": move_to_folder,
    "get_folders": get_folders,
    "draft_reply": draft_reply,
    "flag_for_review": flag_for_review
}