"""
    Summary of `test_delete_product.py`
1. ✅ Delete Existing Product – Ensures valid products can be deleted (200 OK).
2. ✅ Verify Deletion (Optional) – Checks if a deleted product is truly removed (Disabled by default).
3. ❌ Delete Non-Existent Product – Tests API response for invalid or missing product IDs (400/405).

Focus: Validate deletion functionality, error handling, and API stability.
"""
import pytest
from utils.api_client import delete, get
from utils.config import URL
import tests.expected as expected
from utils.helpers import format_assert_message, get_product_ids, get_new_product_id

###  POSITIVE TEST CASE ###
deleted_products = get_product_ids(percentage=100) #list of products we want to delete
delete_verification = False #Delete verification on real scenario

@pytest.mark.parametrize("product_id", deleted_products)  # Delete all products
def test_delete_existing_product(product_id):
    """Verify that deleting an existing product returns 200 OK along with the deleted item details."""
    response = delete(f"{URL}/{product_id}")

    # Check Status Code
    assert response.status_code == expected.STATUS_OK, format_assert_message(
        response, expected.STATUS_OK, product_id
    )

    #  Verify response contains product details
    json_response = response.json()
    assert isinstance(json_response, dict), "Response should be a dictionary"
    assert json_response["id"] == product_id, f"Expected deleted product ID {product_id}, got {json_response['id']}"

    # 📝 Note: In a real scenario, a follow-up GET request should confirm the item is actually deleted.


### 🚨 WRITE-ONLY TEST (DO NOT RUN) ###
@pytest.mark.parametrize("product_id", deleted_products)
@pytest.mark.skipif(not delete_verification, reason="API does not actually delete items.")
def test_verify_deleted_product(product_id):
    """ Verify that a deleted product no longer exists using a GET request (SKIPPED).
        Run only after test_delete_existing_product()"""
    response = get(f"{URL}/{product_id}")

    expected_statuses = [expected.STATUS_NOT_FOUND, expected.STATUS_BAD_REQUEST]
    assert response.status_code in expected_statuses, f"Expected {expected_statuses}, but got {response.status_code}"

### ❌ NEGATIVE TEST CASE ###

large_product_id = get_new_product_id() + 99999 #Non existent product ID
@pytest.mark.parametrize("invalid_product_id", [large_product_id, -1, "abc", "!@#"])
def test_delete_non_existent_product(invalid_product_id):
    """Verify that trying to delete a non-existent product returns 400 Bad Request or 405 Method Not Allowed."""
    response = delete(f"{URL}/{invalid_product_id}")

    expected_statuses = [expected.STATUS_BAD_REQUEST, expected.STATUS_METHOD_NOT_ALLOWED]
    assert response.status_code in expected_statuses, format_assert_message(
        response, expected_statuses, invalid_product_id
    )
