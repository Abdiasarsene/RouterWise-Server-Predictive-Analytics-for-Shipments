import requests

url = "http://127.0.0.1:8000/v1/predict"

data ={
    "Stock_Level": 250,
    "Sales": 80,
    "Transportation_Cost": 75.5,
    "Region": "East",
    "Delivery_Urgency": "On Time",
    "Estimated_Day": 5
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
