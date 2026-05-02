import requests
import json

# --- CONFIGURATION ---
# Aapka token yahan paste karein
access_token = "EAAN9xoW90PoBRQwDOjMtP1WaA80ZA4Hnv7xCE2MDzJCvRi89qNMVjnlgncNCRd4ODZCdLra2YMqoxvUG7lsZCSdXEhK9AqX6jwAzyuCpHFuLegLVsuTcEdbwqdFWxV8k1YKsAkqOyDapk6InoG7U4jCzTZBFtHBzsQvZCMiRAAvnapDMGVzdPlZAmkxwcOgCoGT5ZBAka0ZBdUSSZCQ2aEZCoBcgjHnc3dzT4yQHiorDd4dVDizhHqqAL2mqzwZATyZBsZCWm4j6vfNWdbIHAMRwLrSG5K7WPA5l936KiZCiEhmpf07soYdjYcYXlVXjT84XZArwiEovkZBl661V"

# Meta dashboard (API Setup) se "Phone Number ID" yahan daalein
phone_number_id = "982716530938106" 

# Jis number par message bhejna hai (Country code ke saath, e.g., 91XXXXXXXXXX)
recipient_number = "8141220703"

# API Endpoint
url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Message Data (Template use karna sabse easy aur safe hai)
data = {
    "messaging_product": "whatsapp",
    "to": recipient_number,
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {
            "code": "en_US"
        }
    }
}

# API Call
try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("✅ Message successfully sent!")
        print(response.json())
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.json())
except Exception as e:
    print(f"An error occurred: {e}")