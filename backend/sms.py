"""
<<<<<<< HEAD
sms.py - OTP via MSG91 send-otp API
=======
sms.py - SMS OTP sending via MSG91
>>>>>>> a020675087b727f059f81924023580ac3e3efa17
"""

import os
import requests

<<<<<<< HEAD
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
=======
MSG91_AUTH_KEY = os.environ.get("MSG91_AUTH_KEY", "")
MSG91_SENDER_ID = "SCHEMO"  # Your sender ID (6 chars, register on MSG91)
MSG91_TEMPLATE_ID = os.environ.get("MSG91_TEMPLATE_ID", "")  # Optional: DLT template ID


def send_otp_sms(phone_number, otp):
    """
    Send OTP SMS via MSG91.
    
    Args:
        phone_number (str): 10-digit Indian mobile number
        otp (str): 6-digit OTP code
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not MSG91_AUTH_KEY or MSG91_AUTH_KEY == "your_msg91_auth_key":
        print(f"[SMS] MSG91 not configured. OTP: {otp} for {phone_number}")
        return False
    
    # MSG91 API endpoint
    url = "https://control.msg91.com/api/v5/otp"
    
    # Payload
    payload = {
        "template_id": MSG91_TEMPLATE_ID if MSG91_TEMPLATE_ID else None,
        "mobile": f"91{phone_number}",  # Country code + number
        "authkey": MSG91_AUTH_KEY,
        "otp": otp,
        "sender": MSG91_SENDER_ID,
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"[SMS] OTP sent successfully to {phone_number}")
            return True
        else:
            print(f"[SMS] Failed to send OTP: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print(f"[SMS] Error sending OTP: {e}")
        return False


def send_simple_sms(phone_number, message):
    """
    Send a simple text SMS via MSG91.
    
    Args:
        phone_number (str): 10-digit Indian mobile number
        message (str): SMS text content
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not MSG91_AUTH_KEY:
        print(f"[SMS] MSG91 not configured. Message: {message}")
        return False
    
    url = "https://control.msg91.com/api/v5/flow/"
    
    payload = {
        "authkey": MSG91_AUTH_KEY,
        "mobiles": f"91{phone_number}",
        "sender": MSG91_SENDER_ID,
        "message": message,
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"[SMS] Error: {e}")
        return False
>>>>>>> a020675087b727f059f81924023580ac3e3efa17
