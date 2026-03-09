def register_user(client, url, data):
    """Helper para registrar usuarios"""
    return client.post(url, data, format="json")


def login_user(client, login_url, username, password):
    response = client.post(
        login_url,
        {
            "username": username,
            "password": password
        },
        format="json"
    )

    token = response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    return response