from config import BASE_URL


def compose_url(endpoint):
    return f"{BASE_URL}/{endpoint}/"
