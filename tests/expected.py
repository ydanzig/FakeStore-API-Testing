# expected.py

__all__ = [
    "STATUS_OK",
    "STATUS_NOT_FOUND",
    "STATUS_BAD_REQUEST",
    "STATUS_METHOD_NOT_ALLOWED",
    "STATUS_PAYLOAD_TOO_LARGE",
    "CONTENT_TYPE_JSON",
    "EXPECTED_PRODUCT_KEYS",
    "TEXT_INVALID_ID",
    "EXPECTED_WRONG_COMMAND_MESSAGE"
]

# Expected HTTP Status Codes
STATUS_OK = 200
STATUS_NOT_FOUND = 404
STATUS_BAD_REQUEST = 400
STATUS_METHOD_NOT_ALLOWED = 405
STATUS_PAYLOAD_TOO_LARGE = 413

# Expected Content Types
CONTENT_TYPE_JSON = "application/json; charset=utf-8"
CONTENT_TYPE_HTML = "text/html; charset=utf-8"

# Expected Response Keys for a Product
EXPECTED_PRODUCT_KEYS = ["id", "title", "price", "description", "category", "image"]

# Expected text for invalid id's request
TEXT_INVALID_ID = ""

# Expected error message for wrong command
EXPECTED_WRONG_COMMAND_MESSAGE = f"Cannot POST /products/"