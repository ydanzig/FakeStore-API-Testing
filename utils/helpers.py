import random
from utils.api_client import get
from utils.config import URL
import tests.expected as expected


def get_product_ids(percentage=100, url=URL):
    """
    Fetch all product IDs from the system and return a random subset.

    :param percentage: The percentage of product IDs to return (1-100).
    :param url: URL for fetching the data (default is config URL).
    :return: A list of product IDs (either full list or random subset).
    """
    response = get(url)

    if response.status_code != expected.STATUS_OK:
        raise Exception(f"Failed to fetch products: {response.status_code}")

    products = response.json()
    product_ids = [product["id"] for product in products]

    if not product_ids:
        raise ValueError("No products found in the system.")

    # Ensure we always return at least 1 product
    num_selected = max(1, int(len(product_ids) * (percentage / 100)))

    return random.sample(product_ids, num_selected)  # Select a random subset


def format_assert_message(response, expected_status, sent_data):
    """
    Generates a detailed assertion message for API responses.

    :param response: The API response object.
    :param expected_status: The expected HTTP status code.
    :param sent_data: The request payload that was sent.
    :return: A formatted string with debug information.
    """
    return (
        f"\n🚨 Test Failed!\n"
        f"📤 Sent Data: {sent_data}\n"
        f"✅ Expected Status: {expected_status}\n"
        f"❌ Actual Status: {response.status_code}\n"
        f"📥 Response Body: f{response.json() if response.status_code == {expected.STATUS_OK} else response.text}"
    )

def get_new_product_id():
    """Get a new product ID (not existed) by taking the max existing ID and adding 1."""
    existing_ids = get_product_ids(percentage=100)
    return max(existing_ids, default=0) + 1  # Handle empty list by defaulting to 0

