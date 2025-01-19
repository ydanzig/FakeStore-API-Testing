import threading
import pytest
import time
from utils.api_client import post
from utils.config import URL
import tests.expected as expected

NUM_REQUESTS = 50  # Define how many concurrent requests to send
CONCURRENT_THREADS = 10  # Number of threads to run in parallel

test_product_data = {
    "title": "Stress Test Product",
    "price": 25.99,
    "description": "Performance Testing Product",
    "image": "https://i.pravatar.cc",
    "category": "electronics"
}

results = []  # Store test results

def send_post_request():
    """Sends a single POST request and stores the result."""
    start_time = time.time()  # Measure response time
    response = post(URL, test_product_data)
    end_time = time.time()
    duration = end_time - start_time

    # Collect response info
    results.append({
        "status_code": response.status_code,
        "response_time": duration,
        "response_body": response.json() if response.status_code == expected.STATUS_OK else response.text
    })

@pytest.mark.stress
def test_post_product_stress():
    """ Stress Test: Send multiple concurrent POST requests."""
    threads = []

    for _ in range(NUM_REQUESTS):
        thread = threading.Thread(target=send_post_request)
        threads.append(thread)
        thread.start()

        # Control the number of parallel threads
        if len(threads) >= CONCURRENT_THREADS:
            for t in threads:
                t.join()
            threads.clear()

    # Ensure remaining threads finish
    for t in threads:
        t.join()

    # Analyze Results
    success_count = sum(1 for r in results if r["status_code"] == expected.STATUS_OK)
    failure_count = len(results) - success_count
    avg_response_time = sum(r["response_time"] for r in results) / len(results)

    print(f"\n🔥 Stress Test Summary 🔥")
    print(f"✅ Successful Requests: {success_count}/{NUM_REQUESTS}")
    print(f"❌ Failed Requests: {failure_count}/{NUM_REQUESTS}")
    print(f"⏱ Average Response Time: {avg_response_time:.3f} sec")

    # Assert that at least 90% of requests succeeded
    assert success_count / NUM_REQUESTS >= 0.9, f"Too many failures! Only {success_count}/{NUM_REQUESTS} succeeded."
