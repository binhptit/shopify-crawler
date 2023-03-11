import requests

def request_data(payload):
    url = "https://partners.shopify.com/1095746/api/2023-01/graphql.json"

    headers = {
        "Content-Type": "application/graphql",
        "X-Shopify-Access-Token": "prtapi_02c831dced84b41b8eea11c947112524"
    }

    response = requests.post(url, headers=headers, data=payload)

    return response.json()