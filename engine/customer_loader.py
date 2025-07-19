import json
import os

def load_customer(customer_id):
    path = os.path.join("data", "customer_data.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data.get(customer_id, {})
