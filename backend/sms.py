"""
sms.py - OTP via MSG91 send-otp API
"""

import os
import requests

def send_otp_sms(phone_number: str, otp: str) -> bool:
    """
    Send OTP via MSG91's dedicated OTP API.
    Returns True if sent, False otherwise.
    """
    auth_key = os.environ.get("MSG91_AUTH_KEY", "")
    template_id = os.environ.get("MSG91_TEMPLATE_ID", "")

    if not auth_key:
        print(f"[SMS] MSG91 not configured. OTP for {phone_number}: {otp}")
        return False

    try:
        url = "https://control.msg91.com/api/v5/otp"
        payload = {
            "mobile": f"91{phone_number}",
            "authkey": auth_key,
            "otp": otp,
            "sender": "SCHEMO",
            "otp_length": 6,
            "otp_expiry": 10,
        }
        if template_id:
            payload["template_id"] = template_id

        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json() if resp.content else {}

        if resp.status_code == 200 and data.get("type") == "success":
            print(f"[SMS] OTP sent to {phone_number}")
            return True
        else:
            print(f"[SMS] Failed: {resp.status_code} — {data}")
            return False

    except Exception as e:
        print(f"[SMS] Error: {e}")
        return False


def send_whatsapp_otp(phone_number: str, otp: str) -> bool:
    """Send OTP via MSG91 WhatsApp as fallback."""
    auth_key = os.environ.get("MSG91_AUTH_KEY", "")
    if not auth_key:
        return False
    try:
        url = "https://api.msg91.com/api/v5/whatsapp/whatsapp-outbound-message/bulk/"
        payload = {
            "integrated_number": os.environ.get("MSG91_WHATSAPP_NUMBER", ""),
            "content_type": "template",
            "payload": {
                "to": f"91{phone_number}",
                "type": "text",
                "text": {"body": f"Your Schemo OTP is: *{otp}*\nValid for 10 minutes. Do not share with anyone."}
            }
        }
        import json
        headers = {"authkey": auth_key, "Content-Type": "application/json"}
        resp = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"[WhatsApp OTP Error] {e}")
        return False
