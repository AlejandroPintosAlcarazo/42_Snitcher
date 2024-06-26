import requests
import os
import json
from load_dotenv import load_dotenv

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


if __name__ == "__main__":

    token = generate_token()
    data = []
    i = 0

    while True:
        response = requests.get("https://api.intra.42.fr/v2/users", params={"page": i}, headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code != 200:
            print(response.text)
            exit(1)
        resultado = response.json()
        if not resultado:
            break
        data.append(resultado)
        i += 1

    with open(f"usuarios.txt", "a") as file:
        for j,  elemento in enumerate(data):
            login = elemento["login"]
            file.write(json.dumps(login))
            if j < len(resultado):
                file.write(", ")
            else:
                file.write(".")

