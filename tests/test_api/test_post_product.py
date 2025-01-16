import pytest
from utils.api_client import post

@pytest.mark.parametrize("product_data", [
    {"title": "Valid Product", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},
    {"title": "Another Product", "price": 15.0, "description": "Another test", "image": "https://i.pravatar.cc", "category": "furniture"},
])
def test_post_product_positive(product_data):
    response = post("/products", product_data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["title"] == product_data["title"]

@pytest.mark.parametrize("invalid_data", [
    {},  # Missing fields
    {"title": "No Price"},  # Missing required field
    {"title": "Invalid Price", "price": "string"},  # Invalid type
])
def test_post_product_negative(invalid_data):
    response = post("/products", invalid_data)
    assert response.status_code != 200
