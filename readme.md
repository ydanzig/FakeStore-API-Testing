# 🛠 API Testing with Pytest & Docker

## 📌 Overview
This project provides a **test automation suite** for the [FakeStore API](https://fakestoreapi.com), utilizing **pytest**, **requests**, and **Docker**. The test suite includes:

✅ **Functional Testing** - Validates API behavior with correct input.  
✅ **Negative Testing** - Ensures API handles incorrect input properly.  
✅ **Stress Testing** - Evaluates API performance under load.  
✅ **Security & Edge Case Testing** - Checks for vulnerabilities.

---

## 🚀 Setup Instructions

### **1️⃣ Install Dependencies**
Ensure you have **Python 3.12+** installed, then install the dependencies:

```sh
pip install -r requirements.txt
```

---

### **2️⃣ Run Tests**
You can execute the tests in various ways:

#### ✅ **Run all tests**
```sh
pytest
```

#### ✅ **Run a specific test file**
```sh
pytest tests/test_api/test_post_product.py
```

#### ✅ **Run tests in parallel (faster execution)**
```sh
pytest -n auto
```

#### ✅ **Run only stress tests**
```sh
pytest -m stress
```

---

## **🐳 Running with Docker**

If you prefer to run tests inside a **Docker container**, follow these steps:

### **1️⃣ Build the Docker Image**
```sh
docker build -t api-tests .
```

### **2️⃣ Run Tests Inside Docker**
```sh
docker run --rm api-tests
```

### **3️⃣ Run Specific Tests with Selection Menu**
To select specific tests inside the Docker container, set the `TEST_SELECTION` environment variable:

```sh
docker run --rm -e TEST_SELECTION=1 api-tests
```

| **TEST_SELECTION Value** | **Runs** |
|-----------------|----------------|
| `1` | Get Product Tests |
| `2` | Post Product Tests |
| `3` | Delete Product Tests |
| `4` | Get Products Tests |
| `5` | Stress Test for Products |
| `6` | Run All Tests |

---

## **📂 Project Structure**
```
/YourProject
├── tests/                     # 📂 Test files
│   ├── test_api/              # Functional API tests
│   │   ├── test_get_product.py
│   │   ├── test_get_products.py
│   │   ├── test_post_product.py
│   │   ├── test_delete_product.py
│   ├── stress/                # Stress tests
│   │   ├── test_stress_get_products.py
│   ├── expected.py             # Expected values and assertions
├── utils/                      # 📂 Helper utilities
│   ├── api_client.py           # API interaction functions
│   ├── config.py               # Configuration variables
│   ├── helpers.py              # Helper functions
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container setup
├── pytest.ini                  # Pytest configuration
├── run_tests.py                # Interactive test selection script
├── README.md                   # Project documentation
```

---

## **📜 File Explanations**

### 📁 **Tests** (`/tests`)
- `test_api/` → Functional tests for individual API endpoints.
- `test_stress/` → Stress testing to evaluate API performance.
- `expected.py` → Expected values (status codes, response formats, etc.).

### 📁 **Utilities** (`/utils`)
- `api_client.py` → Defines `GET`, `POST`, and `DELETE` API methods.
- `config.py` → Stores configuration variables (API URLs, timeout settings, etc.).
- `helpers.py` → Contains helper functions for API responses, validation.

### 📜 **Other Files**
- `requirements.txt` → Lists all Python dependencies.
- `Dockerfile` → Configuration for running tests inside a Docker container.
- `pytest.ini` → Pytest configuration for marks, options, and logging.
- `run_tests.py` → Interactive test selection script for running specific tests inside Docker.
- `README.md` → Project documentation (this file!).

---

## **🛡 Security Considerations**
- The stress tests send multiple requests in parallel, which could **overload the API**—use carefully.
- The project does **not** store any sensitive credentials.

---

## **📌 Notes**
- The API is tested against [FakeStore API](https://fakestoreapi.com).
- Modify `config.py` to adjust API endpoints if needed.
- Test failures will show **detailed error messages** using `format_assert_message()` for debugging.

---

## **🔗 Additional Resources**
- [📖 Pytest Documentation](https://docs.pytest.org/)
- [🌍 Requests Documentation](https://docs.python-requests.org/)
- [🐳 Docker Documentation](https://docs.docker.com/)

