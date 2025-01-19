"""
API Test Suite for GET All Products Endpoint

This module contains automated tests for validating the **GET /products** API
of the FakeStore API.

✅ **Test Cases:**
1. **test_sanity_all_products**
   - Ensures a **successful response (200 OK)**.
   - Verifies the API returns **valid JSON data** in **list format**.

2. **test_data_type_integrity**
   - Validates **data types** for all fields.
   - Ensures **each product has the expected keys**.
   - Checks for **unique product IDs** (no duplicates).
   - Verifies **no missing product IDs** within the range."""


import tests.expected as expected
from utils.api_client import get
from utils.config import URL

# Send GET request to /products
response = get(URL)

def test_sanity_all_products():
    """Verify that fetching all products returns a valid JSON list of products."""

    # Check status code
    assert response.status_code == expected.STATUS_OK, (
        f"Expected {expected.STATUS_OK}, but got {response.status_code}"
    )

    # Verify content type
    assert response.headers["Content-Type"] == expected.CONTENT_TYPE_JSON, (
        f"Unexpected content type: {response.headers['Content-Type']}"
    )

def test_data_type_integrity():
    # Parse JSON response
    json_response = response.json()

    # Verify response is a list
    assert isinstance(json_response, list), "Response should be a list of products"
    assert len(json_response) > 0, "Product list should not be empty"

    # Check the structure of each product
    seen_ids = set()  # Track unique product IDs
    min_id, max_id = float("inf"), float("-inf")  # Initialize min/max to extreme values
    for product in json_response:
        assert isinstance(product, dict), "Each product should be a dictionary"

        # Check required keys exist
        assert all(key in product for key in expected.EXPECTED_PRODUCT_KEYS), "Missing keys in a product"

        # Check data types
        assert isinstance(product["id"], int), "ID should be an integer"
        assert isinstance(product["title"], str) and product["title"], "Title should be a non-empty string"
        assert isinstance(product["price"], (int, float)) and product["price"] > 0, "Price should be a positive number"
        assert isinstance(product["description"], str) and product[
            "description"], "Description should be a non-empty string"
        assert isinstance(product["category"], str) and product["category"], "Category should be a non-empty string"
        assert isinstance(product["image"], str) and product["image"].startswith(
            "http"), "Image URL should start with http"
        assert isinstance(product["rating"], dict), "Rating should be a dictionary"

        # Validate rating values
        assert "rate" in product["rating"] and isinstance(product["rating"]["rate"],
            (int, float)), "Rate should be a float or int"
        assert product["rating"]["rate"] >= 0, f"Rate should be >= 0, but got {product['rating']['rate']}"
        assert "count" in product["rating"] and isinstance(product["rating"]["count"],
             int), "Count should be an integer"
        assert product["rating"]["count"] >= 0, f"Count should be >= 0, but got {product['rating']['count']}"

        # Ensure Product IDs are unique
        assert product["id"] not in seen_ids, f"Duplicate product ID found: {product['id']}"
        seen_ids.add(product["id"])

        # min/max ID tracking
        min_id, max_id = min(min_id, product["id"]), max(max_id, product["id"])

    # Ensuring no missing items
    actual_ids = seen_ids

    # Expected sequence of IDs
    expected_ids = set(range(min_id, max_id + 1))

    # Detect missing IDs
    missing_ids = expected_ids - actual_ids  # Set difference

    # Assert that no IDs are missing
    assert not missing_ids, f"Missing product IDs detected: {sorted(missing_ids)}" #Assert on non-empty set (missing items)