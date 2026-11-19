TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_emails",
            "description": "List every email: id | from | subject | folder. Bodies are not shown.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read one email in full, including the body",
            "parameters": {
                "type": "object",
                "properties": {"email_id": {"type": "string"}},
                "required": ["email_id"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_to_folder",
            "description": "Move an email into a folder. Use short lowercase names and reuse existing folders.",
            "parameters": {
                "type": "object",
                "properties": {"email_id": {"type": "string"}, "folder": {"type": "string"}},
                "required": ["email_id", "folder"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_folders",
            "description": "List every folder currently in use.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_reply",
            "description": "Save a draft reply for a human to review. Use this whenever a real person asked a question or is waiting for an asnwer. Nothing is ever sent.",
            "parameters": {
                "type": "object",
                "properties": {"email_id": {"type": "string"}, "body": {"type": "string"}},
                "required": ["email_id", "body"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "flag_for_review",
            "description": "Flag an email for human review, with a reason.",
            "parameters": {
                "type": "object",
                "properties": {"email_id": {"type": "string"}, "reason": {"type": "string"}},
                "required": ["email_id", "reason"],
            }
        }
    },
]