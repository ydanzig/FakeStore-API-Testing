import random
from utils.api_client import get

def get_product_ids(url, percentage=100):
    """
    Fetch all product IDs from the system and return a random subset.

    :param percentage: The percentage of product IDs to return (1-100).
    :param: url for fetching the data.
    :return: A list of product IDs (either full list or random subset).
    """
    response = get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch products: {response.status_code}")

    products = response.json()
    product_ids = [product["id"] for product in products]

    if not product_ids:
        raise ValueError("No products found in the system.")

    # Ensure we always return at least 1 product
    num_selected = max(1, int(len(product_ids) * (percentage / 100)))

    return random.sample(product_ids, num_selected)  # Select a random subset

