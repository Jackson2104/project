import requests
import base64

def send_bulk_sms(phone_numbers, message, api_key, secret_key):
    """
    Tuma SMS kwa list ya namba za simu kwa kutumia Beem Africa.
    """
    url = "https://sms.beem.africa/v1/send"

    # Andaa authorization header
    credentials = f"{api_key}:{secret_key}"
    token = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    data = {
        "source_addr": "kijiji",  # Jina litakaloonekana (unaweza kubadilisha)
        "encoding": "0",
        "schedule_time": "",  # Acha tupu kama hutaki kupanga muda
        "message": message,
        "recipients": [{"recipient_id": str(i+1), "dest_addr": number} for i, number in enumerate(phone_numbers)]
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code, response.text
