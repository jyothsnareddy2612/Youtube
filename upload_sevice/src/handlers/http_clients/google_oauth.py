import requests


def exchange_code_for_user(token_data: dict):
    token_response = requests.post(
        "https://oauth2.googleapis.com/token", data=token_data
    ).json()
    access_token = token_response.get("access_token")

    return requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
