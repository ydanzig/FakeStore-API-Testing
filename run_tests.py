import sys
import os

def display_menu():
    """Display a menu of available tests and get user selection via environment variable."""
    tests = {
        "1": "tests/test_api/test_get_product.py",
        "2": "tests/test_api/test_post_product.py",
        "3": "tests/test_api/test_delete_product.py",
        "4": "tests/test_api/test_get_products.py",
        "5": "tests/stress/test_stress_get_products.py",
        "6": "ALL TESTS"
    }

    print("\n📌 Available Tests:")
    for key, test in tests.items():
        print(f"{key}. {test}")

    # Read selection from an environment variable
    choice = os.environ.get("TEST_SELECTION")

    # If no selection is provided, default to running all tests
    if choice is None or choice not in tests:
        print("❌ No valid test selection found. Running all tests by default.")
        return "tests"

    return tests[choice]

def run_tests():
    """Run pytest based on user selection."""
    test_to_run = display_menu() # test filename path
    command = f"pytest {test_to_run}"
    print(f"\n🚀 Running: {command}\n")
    os.system(command)
    sys.exit()

if __name__ == "__main__":
    run_tests()
