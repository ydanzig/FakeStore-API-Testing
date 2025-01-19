"""
 API Test Suite for POST Product Endpoint

This module contains automated tests for validating the **POST /products** API
of the FakeStore API.

📝 **Purpose:**
- Ensures **products can be added correctly**.
- Validates **status codes, response structures, and data integrity**.
- Checks **edge cases, invalid inputs, and security vulnerabilities**.

✅ **Test Cases:**
1. **test_post_product_positive**
   - Ensures valid product creation with **200 OK** response.
   - Verifies the response contains the correct **structure and data**.

🚨 **Negative Test Cases:**
2. **test_invalid_json** → Ensures rejection of **invalid or empty JSON**.
3. **test_missing_fields** → Checks that **missing fields** trigger errors.
4. **test_wrong_data_types** → Ensures **wrong field types** are rejected.
5. **test_invalid_field_values** → Detects **empty or incorrectly formatted values**.
6. **test_invalid_price_values** → Prevents **negative or zero prices** (if applicable).
7. **test_unexpected_fields** → Blocks **extra, unexpected fields**.
8. **test_large_values** → Ensures **large inputs** don’t crash the system.
9. **test_invalid_image_formats** → Prevents **non-image file uploads** as images.
10.**test_security_hacker_attempts** → Blocks **SQL Injection, XSS, and other threats**.

🔍 **Test Coverage:**
- ✅ **Successful Product Creation**
- ✅ **Proper Response Validation**
- ✅ **Error Handling for Invalid Inputs**
- ✅ **Security & Injection Protection**
- ✅ **Edge Case Handling (Large Inputs, Unexpected Data)**"""

import pytest
from utils.api_client import post
from utils.config import URL, LARGE_TITLE, LARGE_PRICE, LARGE_IMAGE_URL
import tests.expected as expected
from utils.helpers import format_assert_message

### ✅ POSITIVE TEST CASES ###
@pytest.mark.parametrize("product_data", [
    {"title": "Valid Product", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},
    {"title": "Another Product", "price": 15, "description": "Another test", "image": "https://i.pravatar.cc", "category": "furniture"},
])
def test_post_product_positive(product_data):
    response = post(URL, product_data)
    assert response.status_code == expected.STATUS_OK
    json_response = response.json()
    #validate response structure
    assert isinstance(json_response, dict), "Response should be a dictionary"
    assert all(key in json_response for key in expected.EXPECTED_PRODUCT_KEYS), "Missing keys in response"
    assert isinstance(json_response["id"], int), (
        f"New ID should be an integer but {json_response['id']} is {type(json_response['id'])}"
    )
    #Validates data integrity -Ensures returned data matches input.
    for product_key in expected.EXPECTED_PRODUCT_KEYS:
        if product_key == "id":
            continue # Skip ID because it's auto-generated
        else:
            assert json_response[product_key] == product_data[product_key], (
                f"Mismatch in {product_key}: expected {product_data[product_key]}, got {json_response[product_key]}"
            )

### ❌ NEGATIVE TEST CASES ###
# If the API actually creates products, an additional check should be done to ensure no product is stored.

### 1.INVALID JSON / EMPTY DATA ###
@pytest.mark.parametrize("invalid_data", [
    None,  # No data at all (invalid JSON)
    "",  # Empty string instead of JSON
    "Not a JSON",  # Plain text instead of JSON
    12345,  # Number instead of JSON object
    [],  # Empty list instead of an object
])
def test_invalid_json(invalid_data):
    """Verify that posting invalid JSON or empty data returns 400"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)

### 2.MISSING OR NULL FIELDS ###
@pytest.mark.parametrize("invalid_data", [
    {"title": None, "price": None, "description": None, "image": None, "category": None},  # All fields `null`
    {"title": "Missing Price"},  # Missing required `price` field
    {"price": 20.5},  # Missing required `title` field
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc"},  # Missing category
])
def test_missing_fields(invalid_data):
    """Verify that missing or null fields result in 400 Bad Request"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)


### 3.WRONG DATA TYPES ###
@pytest.mark.parametrize("invalid_data", [
    {"title": "Valid", "price": "string", "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  # `price` must be a number
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": 123},  # `category` must be a string
    {"title": "Valid", "price": None, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  # `price` is `None`
])
def test_wrong_data_types(invalid_data):
    """Verify that wrong data types result in 400 Bad Request"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)


### 4.EMPTY OR INVALID FIELD VALUES ###
@pytest.mark.parametrize("invalid_data", [
    {"title": "", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  # Empty `title`
    {"title": "Valid", "price": 20.5, "description": "", "image": "https://i.pravatar.cc", "category": "electronics"},  # Empty `description`
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "", "category": "electronics"},  # Empty `image`
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "invalid_url", "category": "electronics"},  # Invalid `image` URL format
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": ""},  # Empty `category`
])
def test_invalid_field_values(invalid_data):
    """Verify that empty or invalid field values result in 400 Bad Request"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)


### 5.INVALID PRICE VALUES ###
@pytest.mark.parametrize("invalid_data", [
    {"title": "Valid", "price": -10, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  # Negative price
    {"title": "Valid", "price": 0, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  # Zero price (if not allowed)
])
def test_invalid_price_values(invalid_data):
    """Verify that invalid price values result in 400 Bad Request"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)


### 6.UNEXPECTED FIELDS ###
@pytest.mark.parametrize("invalid_data", [
    {"unexpected_field": "random value"},  # Completely wrong structure
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics", "extra_field": "Not allowed"},  # Unexpected extra field
])
def test_unexpected_fields(invalid_data):
    """Verify that unexpected fields result in 400 Bad Request"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)

### 7.LARGE VALUE TESTING ###
@pytest.mark.parametrize("invalid_data", [
    {"title": LARGE_TITLE, "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},
    {"title": "Valid", "price": LARGE_PRICE, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},
    {"title": "Valid", "price": 20.5, "description": "Test", "image": LARGE_IMAGE_URL, "category": "electronics"},
])
def test_large_values(invalid_data):
    """Verify that moderately large values result in 512/400 large data Request"""
    response = post(URL, invalid_data)
    expected_status = [expected.STATUS_PAYLOAD_TOO_LARGE, expected.STATUS_BAD_REQUEST]
    assert response.status_code in expected_status, format_assert_message(
        response, expected_status, invalid_data
    )

### 8.INVALID IMAGE FORMATS ###
@pytest.mark.parametrize("invalid_data", [
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://example.com/image.txt", "category": "electronics"},  #  Wrong format (text file)
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://example.com/image.mp3", "category": "electronics"},  #  Audio file
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://example.com/image.exe", "category": "electronics"},  #  Executable file
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA", "category": "electronics"},  #  Base64-encoded image
])
def test_invalid_image_formats(invalid_data):
    """Verify that invalid image formats result in 400 Bad Request"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)

###  9.SECURITY & HACKER TESTING ###
@pytest.mark.parametrize("invalid_data", [
    {"title": "' OR 1=1 --", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  #  SQL Injection attempt
    {"title": "<script>alert('XSS')</script>", "price": 20.5, "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  #  XSS Injection
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://evil.com/virus.js", "category": "electronics"},  #  Image linking to a JavaScript file
    {"title": "Valid", "price": "DROP TABLE products;", "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  #  SQL Command Injection
    {"title": "Valid", "price": "import os; os.system('rm -rf /')", "description": "Test", "image": "https://i.pravatar.cc", "category": "electronics"},  #  Code Injection
    {"title": "Valid", "price": 20.5, "description": "Test", "image": "https://www.evil-site.com/malware.png", "category": "electronics"},  #  External malware URL
])
def test_security_hacker_attempts(invalid_data):
    """Verify that security vulnerabilities (SQL Injection, XSS, Code Injection) are blocked"""
    response = post(URL, invalid_data)
    assert response.status_code == expected.STATUS_BAD_REQUEST, format_assert_message(
        response, expected.STATUS_BAD_REQUEST, invalid_data)