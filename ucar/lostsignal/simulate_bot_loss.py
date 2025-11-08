import requests

url = "http://127.0.0.1:8000/api/pingloss/"
data = {
    "description": "Состояние устройства изменилось",
    "device_id": "1111",
    "ping_status": "up"
}

response = requests.post(url, json=data)
print("Status code:", response.status_code)
print("Response:", response.json())


