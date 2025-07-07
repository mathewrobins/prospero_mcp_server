import requests
import yaml

class ProsperoClient:
    def __init__(self):
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        self.api_key = config['prospero']['api_key']
        self.endpoint = config['prospero']['endpoint']

    def find_email(self, domain, first_name, last_name):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "domain": domain,
            "first_name": first_name,
            "last_name": last_name
        }
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}