
@pytest.mark.parametrize("num_products", [5, 10, 20])
def test_get_all_products(num_products):
    """Verify that fetching all products returns a list with multiple product items"""
    response = get(BASE_ENDPOINT)

    # ✅ Verify status code
    assert response.status_code == 200

    # ✅ Verify content type
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    # ✅ Verify response is a list
    json_response = response.json()
    assert isinstance(json_response, list), "Expected a list of products"
    assert len(json_response) >= num_products, f"Expected at least {num_products} products"

