import threading
import pytest
import time
from utils.api_client import post
from utils.config import URL
import tests.expected as expected

#Configuration for Stress Test
NUM_REQUESTS = 50  # Total number of POST requests to send
CONCURRENT_THREADS = 10  # Maximum number of parallel threads

# Sample product data to send in POST requests
test_product_data = {
    "title": "Stress Test Product",
    "price": 25.99,
    "description": "Performance Testing Product",
    "image": "https://i.pravatar.cc",
    "category": "electronics"
}

# Store results of all API calls
results = []


def send_post_request():
    """
    Sends a single POST request and records the response.

    - Measures response time.
    - Stores HTTP status code, response time, and response content.
    """
    start_time = time.time()  # Start timer
    response = post(URL, test_product_data)  # Send request
    end_time = time.time()  # Stop timer
    duration = end_time - start_time  # Calculate duration

    # Store results for later analysis
    results.append({
        "status_code": response.status_code,
        "response_time": duration,
        "response_body": response.json() if response.status_code == expected.STATUS_OK else response.text
    })


@pytest.mark.stress
def test_post_product_stress():
    """
      Stress Test: Sends multiple concurrent POST requests to test API performance under load.

    - Uses threading to send requests concurrently.
    - Analyzes success/failure rates.
    - Computes average response time.
    - Fails if success rate < 90%.
    """
    threads = []

    # Send multiple requests in parallel
    for _ in range(NUM_REQUESTS):
        thread = threading.Thread(target=send_post_request)
        threads.append(thread)
        thread.start()

        # Control number of parallel threads to avoid excessive load
        if len(threads) >= CONCURRENT_THREADS:
            for t in threads:
                t.join()
            threads.clear()  # Reset thread list

    # Ensure remaining threads finish execution
    for t in threads:
        t.join()

    # Analyze test results
    success_count = sum(1 for r in results if r["status_code"] == expected.STATUS_OK)
    failure_count = len(results) - success_count
    avg_response_time = sum(r["response_time"] for r in results) / len(results)

    # Display Stress Test Summary
    print(f"\n🔥 Stress Test Summary 🔥")
    print(f"✅ Successful Requests: {success_count}/{NUM_REQUESTS}")
    print(f"❌ Failed Requests: {failure_count}/{NUM_REQUESTS}")
    print(f"⏱ Average Response Time: {avg_response_time:.3f} sec")

    # Test Fails if success rate < 90%
    assert success_count / NUM_REQUESTS >= 0.9, f"Too many failures! Only {success_count}/{NUM_REQUESTS} succeeded."
