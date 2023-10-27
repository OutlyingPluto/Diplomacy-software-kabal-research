import requests
import os

# data = response.json() # for json formatted-data

def Retrieve():
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get("api.com/<route>?api_key={whatever}?arg1=<>?arg2=<>...argn=<>")
        response.raise_for_status()
    except requests.RequestException:
        return None

        # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None