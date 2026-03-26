"""
sms.py - SMS OTP sending via MSG91
"""

import os
import requests

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
