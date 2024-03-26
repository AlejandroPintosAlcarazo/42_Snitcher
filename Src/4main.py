import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


def generate_token():
    url = "https://api.intra.42.fr/oauth/token"
    body = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }

    response = requests.post(url, json=body)
    print(response)
    token = response.json()["access_token"]
    return token
    
def get_campus_info(token):

    i = 1
    campus_list = []
    while True:
        response = requests.get("https://api.intra.42.fr/v2/campus", params={"page": i}, headers={
            "Authorization": f"Bearer {token}"
        })

        if response.status_code != 200:
            print(response.text)
            exit(1)

        campuses = response.json()
        campus_list.extend(campuses)
        i += 1

        if not campuses:
            break

    campus_info = {}
    for campus in campus_list:
        campus_info[campus['name']] = campus['id']

    return campus_info


if __name__ == "__main__":

    token = generate_token()
    campus_info = get_campus_info(token)

    for name, campus_id in campus_info.items():
        print(f"Campus Name: {name}, Campus ID: {campus_id}")

