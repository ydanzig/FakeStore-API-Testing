import requests

request_timeout = 10  # Timeout in seconds

def get(url, timeout=request_timeout):
    """Send a GET request and return the raw response."""
    return requests.get(url, timeout=timeout)

def post(url, data, timeout=request_timeout):
    """Send a POST request and return the raw response."""
    return requests.post(url, json=data, timeout=timeout)

def delete(url, timeout=request_timeout):
    """Send a DELETE request and return the raw response."""
    return requests.delete(url, timeout=timeout)
