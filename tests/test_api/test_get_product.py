import pytest
import tests.expected as expected
from utils.api_client import get, post
from utils.helpers import get_product_ids
from utils.config import URL

positive_coverage = 100 #Positive percentage of site products
negative_coverage = 5 #Negative percentage of site products
positive_product_ids = get_product_ids(URL, positive_coverage) #List for positive test
negative_product_ids = get_product_ids(URL, negative_coverage) #List for negative test
false_ids = [-1, 0, 10000, "abc", "!@#"]

### ✅ POSITIVE TEST CASES ###
@pytest.mark.parametrize("product_id", positive_product_ids)
def test_structure_sanity(product_id):
    """Verify that fetching a product with a valid ID returns 200 and correct content type and json keys"""
    response = get(f"{URL}/{product_id}")

    # Verify status code
    assert response.status_code == expected.STATUS_OK, f"Expected {expected.STATUS_OK}, but got {response.status_code}"

    # Verify content type
    assert response.headers["Content-Type"] == expected.CONTENT_TYPE_JSON

    # Verify response structure an id match
    json_response = response.json()
    assert isinstance(json_response, dict), "Response should be a dictionary"
    assert all(key in json_response for key in expected.EXPECTED_PRODUCT_KEYS), "Missing keys in response"
    assert json_response["id"] == product_id #Vlidate correct product load.

@pytest.mark.parametrize("product_id", positive_product_ids)
def test_data_type_integrity(product_id):
    response = get(f"{URL}/{product_id}")
    json_response = response.json()
    # Check data types and data integrity
    assert isinstance(json_response["id"], int), "ID should be an integer"
    assert isinstance(json_response["title"], str) and json_response["title"], "Title should be a non-empty string"
    assert isinstance(json_response["price"], (int, float)) and json_response["price"] > 0, "Price should be a positive number"
    assert isinstance(json_response["description"], str) and json_response["description"], "Description should be a non-empty string"
    assert isinstance(json_response["category"], str) and json_response["category"], "Category should be a non-empty string"
    assert isinstance(json_response["image"], str) and json_response["image"].startswith("http"), "Image URL should be a valid string starting with http"
    assert isinstance(json_response["rating"], dict), "Rating should be a dictionary"
    assert "rate" in json_response["rating"] and isinstance(json_response["rating"]["rate"],
                                                            (int, float)), "Rate should be a float or int"
    assert json_response["rating"]["rate"] >= 0, f"Rate should be >= 0, but got {json_response['rating']['rate']}"
    assert "count" in json_response["rating"] and isinstance(json_response["rating"]["count"],
                                                             int), "Count should be an integer"
    assert json_response["rating"]["count"] >= 0, f"Count should be >= 0, but got {json_response['rating']['count']}"

    # Check if the image URL is accessible
    img_url = json_response["image"]
    img_response = get(img_url)
    assert img_response.status_code == expected.STATUS_OK, f"Broken image URL: {img_url}"


### ❌ NEGATIVE TEST CASES ###
@pytest.mark.parametrize("invalid_id", false_ids)
def test_false_ids(invalid_id):
    """Verify that fetching a product with an invalid ID returns a 404 or appropriate error response"""
    response = get(f"{URL}/{invalid_id}")

    # Verify proper error handling
    assert (response.status_code in [expected.STATUS_NOT_FOUND, expected.STATUS_BAD_REQUEST],
            f"Expected {expected.STATUS_NOT_FOUND} or {expected.STATUS_BAD_REQUEST}, but got {response.status_code}")

    # Verify result is empty (not showing any product)
    response_text = response.text.strip()
    assert response_text == expected.TEXT_INVALID_ID, f"Expected {expected.TEXT_INVALID_ID} but got {response_text}"

@pytest.mark.parametrize("product_id",  negative_product_ids)
def test_wrong_command(product_id):
    """Verify that calling the GET endpoint with an incorrect HTTP method (POST) is rejected"""
    response = post(f"{URL}/{product_id}", {})  # Sending an empty body as POST is invalid

    # Expected error: Method Not Allowed (405)
    assert response.status_code == expected.STATUS_METHOD_NOT_ALLOWED, (f"Expected {expected.STATUS_METHOD_NOT_ALLOWED},"
                                                                        f" but got {response.status_code}")
    # Verify response body contains correct error message
    response_text = response.text.strip()
    expected_error_text = f"Cannot POST /products/{product_id}"
    assert expected_error_text in response_text, (
        f"Expected error message '{expected_error_text}', but got '{response_text}'"
    )