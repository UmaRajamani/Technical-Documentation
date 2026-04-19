# TaskFlow API — Integration Guide

> Connect your application to TaskFlow's project management platform. Automate task creation, sync team data, and trigger workflows — all via REST API.

[![API Version](https://img.shields.io/badge/API-v3.1-blue)](https://docs.taskflow.io)
[![SDK](https://img.shields.io/badge/Python_SDK-1.8.0-green)](https://pypi.org/project/taskflow-sdk)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen)](https://status.taskflow.io)

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Step-by-Step: Common Workflows](#step-by-step-common-workflows)
  - [Create a project and add tasks](#1-create-a-project-and-add-tasks)
  - [Assign tasks to team members](#2-assign-tasks-to-team-members)
  - [Update task status](#3-update-task-status)
  - [List overdue tasks](#4-list-overdue-tasks)
  - [Set up a webhook](#5-set-up-a-webhook)
- [Python SDK](#python-sdk)
- [cURL Examples](#curl-examples)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)
- [Support](#support)

---

## Overview

The TaskFlow API lets you integrate task and project management into any application. Common use cases include:

- **Support tools** — auto-create tasks from customer tickets
- **Dev workflows** — create tasks from GitHub issues or Jira bugs
- **Reporting dashboards** — pull task data into analytics tools
- **Automation** — trigger workflows when task status changes

**Base URL:** `https://api.taskflow.io/v3`  
**Format:** All requests and responses use JSON  
**Auth:** Bearer token (OAuth 2.0 or API key)

---

## Quick Start

Get a task list in 60 seconds:

```bash
# 1. Export your API key
export TASKFLOW_API_KEY="tf_live_xxxxxxxxxxxx"

# 2. Fetch your projects
curl https://api.taskflow.io/v3/projects \
  -H "Authorization: Bearer $TASKFLOW_API_KEY"

# 3. Create your first task
curl -X POST https://api.taskflow.io/v3/tasks \
  -H "Authorization: Bearer $TASKFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Set up API integration",
    "project_id": "proj_abc123",
    "assignee_id": "usr_xyz789",
    "due_date": "2024-04-01",
    "priority": "high"
  }'
```

---

## Authentication

TaskFlow supports two authentication methods:

### Option A — API Key (recommended for server-to-server)

Generate an API key from [Settings → API Keys](https://app.taskflow.io/settings/api-keys).

Pass it as a Bearer token in every request:

```
Authorization: Bearer tf_live_xxxxxxxxxxxx
```

### Option B — OAuth 2.0 (recommended for user-facing apps)

Use OAuth when your app acts on behalf of individual users.

**Step 1 — Redirect the user:**
```
https://app.taskflow.io/oauth/authorize
  ?client_id=YOUR_CLIENT_ID
  &redirect_uri=https://yourapp.com/callback
  &scope=tasks:read tasks:write projects:read
  &response_type=code
```

**Step 2 — Exchange the code for a token:**
```bash
curl -X POST https://api.taskflow.io/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "authorization_code",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "code": "AUTH_CODE_FROM_REDIRECT",
    "redirect_uri": "https://yourapp.com/callback"
  }'
```

**Step 3 — Use the access token:**
```
Authorization: Bearer ACCESS_TOKEN
```

Tokens expire after **8 hours**. Use the `refresh_token` to obtain a new one without re-authenticating.

---

## Step-by-Step: Common Workflows

### 1. Create a project and add tasks

**Step 1 — Create the project:**

```python
import os
import requests

BASE_URL = "https://api.taskflow.io/v3"
HEADERS = {
    "Authorization": f"Bearer {os.environ['TASKFLOW_API_KEY']}",
    "Content-Type": "application/json"
}

project = requests.post(f"{BASE_URL}/projects", headers=HEADERS, json={
    "name": "Q2 Product Launch",
    "description": "All tasks for the Q2 product launch",
    "color": "#4F46E5",
    "visibility": "team"
}).json()

project_id = project["id"]
print(f"Created project: {project_id}")
```

**Step 2 — Add tasks to the project:**

```python
tasks = [
    {"title": "Write launch blog post",      "priority": "high",   "due_date": "2024-04-10"},
    {"title": "Update pricing page",          "priority": "high",   "due_date": "2024-04-08"},
    {"title": "Send launch email campaign",   "priority": "medium", "due_date": "2024-04-15"},
    {"title": "Post on social media",         "priority": "low",    "due_date": "2024-04-15"},
]

created_tasks = []
for task_data in tasks:
    task_data["project_id"] = project_id
    task = requests.post(f"{BASE_URL}/tasks", headers=HEADERS, json=task_data).json()
    created_tasks.append(task)
    print(f"  Created task [{task['id']}]: {task['title']}")
```

---

### 2. Assign tasks to team members

**Step 1 — Fetch your team members:**

```python
members = requests.get(f"{BASE_URL}/workspace/members", headers=HEADERS).json()

# Build a lookup: email → user ID
member_map = {m["email"]: m["id"] for m in members["data"]}
print(member_map)
# {'alice@acme.com': 'usr_001', 'bob@acme.com': 'usr_002', ...}
```

**Step 2 — Assign a task:**

```python
task_id = created_tasks[0]["id"]
assignee_id = member_map.get("alice@acme.com")

updated = requests.patch(
    f"{BASE_URL}/tasks/{task_id}",
    headers=HEADERS,
    json={"assignee_id": assignee_id}
).json()

print(f"Assigned '{updated['title']}' to {updated['assignee']['name']}")
```

---

### 3. Update task status

Tasks move through these statuses: `todo` → `in_progress` → `in_review` → `done`

```python
task_id = created_tasks[0]["id"]

# Mark as in progress
response = requests.patch(
    f"{BASE_URL}/tasks/{task_id}",
    headers=HEADERS,
    json={
        "status": "in_progress",
        "started_at": "2024-03-15T09:00:00Z"
    }
)

task = response.json()
print(f"Status updated to: {task['status']}")

# Mark as done
response = requests.patch(
    f"{BASE_URL}/tasks/{task_id}",
    headers=HEADERS,
    json={"status": "done"}
)
print(f"Task completed at: {response.json()['completed_at']}")
```

---

### 4. List overdue tasks

```python
from datetime import date

today = date.today().isoformat()

# Fetch all tasks past their due date that are not done
response = requests.get(
    f"{BASE_URL}/tasks",
    headers=HEADERS,
    params={
        "due_before": today,
        "status": "todo,in_progress,in_review",  # exclude 'done'
        "project_id": project_id,
        "limit": 50
    }
)

overdue = response.json()["data"]
print(f"Found {len(overdue)} overdue tasks:\n")

for task in overdue:
    days_late = (date.today() - date.fromisoformat(task["due_date"])).days
    print(f"  [{days_late}d late] {task['title']} — {task.get('assignee', {}).get('name', 'Unassigned')}")
```

---

### 5. Set up a webhook

Webhooks notify your server in real time when TaskFlow events occur.

**Step 1 — Register your endpoint:**

```bash
curl -X POST https://api.taskflow.io/v3/webhooks \
  -H "Authorization: Bearer $TASKFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/webhooks/taskflow",
    "events": [
      "task.created",
      "task.status_changed",
      "task.assigned",
      "task.overdue"
    ],
    "secret": "your_signing_secret_here"
  }'
```

**Step 2 — Handle the webhook in Python (Flask example):**

```python
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
WEBHOOK_SECRET = "your_signing_secret_here"

@app.route("/webhooks/taskflow", methods=["POST"])
def handle_taskflow_webhook():
    # Step 1: Verify the signature
    signature = request.headers.get("X-TaskFlow-Signature", "")
    payload = request.get_data(as_text=True)
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        return jsonify({"error": "Invalid signature"}), 401

    # Step 2: Parse the event
    event = request.json
    event_type = event["type"]
    task = event["data"]["task"]

    # Step 3: Handle the event
    if event_type == "task.status_changed":
        print(f"Task '{task['title']}' moved to '{task['status']}'")
        # Your logic here — e.g., notify Slack, update your DB

    elif event_type == "task.overdue":
        print(f"OVERDUE: '{task['title']}' — assigned to {task.get('assignee', {}).get('name')}")
        # Your logic — e.g., send reminder email

    # Step 4: Always return 200 to acknowledge receipt
    return jsonify({"received": True}), 200
```

> **Always return HTTP 200** immediately after receiving the webhook. If your handler takes longer than 5 seconds, TaskFlow will retry the delivery.

---

## Python SDK

Install the official SDK:

```bash
pip install taskflow-sdk
```

The SDK wraps the REST API with typed objects and automatic retry/rate-limit handling:

```python
from taskflow import TaskFlowClient

client = TaskFlowClient(api_key="tf_live_xxxxxxxxxxxx")

# Create a task
task = client.tasks.create(
    title="Review API documentation",
    project_id="proj_abc123",
    priority="high",
    due_date="2024-04-01"
)

# Update status
task.update(status="in_progress")

# List all tasks in a project
tasks = client.tasks.list(project_id="proj_abc123", status="todo")
for t in tasks:
    print(t.title, t.due_date)
```

---

## cURL Examples

```bash
# List all projects
curl https://api.taskflow.io/v3/projects \
  -H "Authorization: Bearer $TASKFLOW_API_KEY"

# Create a task
curl -X POST https://api.taskflow.io/v3/tasks \
  -H "Authorization: Bearer $TASKFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"New task","project_id":"proj_abc123","priority":"medium"}'

# Update task status
curl -X PATCH https://api.taskflow.io/v3/tasks/task_xyz789 \
  -H "Authorization: Bearer $TASKFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'

# Delete a task
curl -X DELETE https://api.taskflow.io/v3/tasks/task_xyz789 \
  -H "Authorization: Bearer $TASKFLOW_API_KEY"
```

---

## Error Handling

All errors return a consistent JSON structure:

```json
{
  "error": {
    "code": "task_not_found",
    "message": "No task found with ID task_xyz789",
    "status": 404,
    "request_id": "req_abc123"
  }
}
```

| HTTP Status | Error Code | Meaning |
|-------------|------------|---------|
| `400` | `validation_error` | Missing or invalid request parameters |
| `401` | `unauthorized` | Invalid or missing API key |
| `403` | `forbidden` | Key lacks permission for this resource |
| `404` | `not_found` | Resource does not exist |
| `409` | `conflict` | Resource already exists (e.g. duplicate project name) |
| `429` | `rate_limit_exceeded` | Too many requests — see `Retry-After` header |
| `500` | `internal_error` | TaskFlow server error — retry with backoff |

---

## Rate Limits

| Plan | Requests/minute | Requests/day |
|------|----------------|-------------|
| Free | 30 | 1,000 |
| Pro | 300 | 50,000 |
| Business | 1,000 | 500,000 |
| Enterprise | Unlimited | Unlimited |

When rate limited, the response includes:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 12
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1710076812
```

Implement exponential backoff: wait `Retry-After` seconds, then retry.

---

## Support

- **Documentation:** [docs.taskflow.io](https://docs.taskflow.io)
- **API Status:** [status.taskflow.io](https://status.taskflow.io)
- **Developer Community:** [community.taskflow.io](https://community.taskflow.io)
- **Email Support:** devs@taskflow.io (Pro and above)
- **GitHub Issues:** [github.com/taskflow/api-issues](https://github.com/taskflow/api-issues)

---

*Last updated: March 2024 · API v3.1 · SDK v1.8.0*
