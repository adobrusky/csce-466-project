import requests
import pytest


def test_get_all_customers_status_code():
    response = requests.get("http://127.0.0.1:5000/customers")
    assert response.status_code == 200


def test_get_all_customers_json_format():
    response = requests.get("http://127.0.0.1:5000/customers")
    assert response.headers["Content-Type"] == "application/json"

    customers = response.json()
    assert isinstance(customers, list)

    for customer in customers:
        assert "id" in customer
        assert "first_name" in customer
        assert "last_name" in customer


def test_get_customer_by_id_status_code():
    response = requests.get("http://127.0.0.1:5000/customers/1")
    assert response.status_code == 200


def test_get_customer_by_id_json_format():
    response = requests.get("http://127.0.0.1:5000/customers/1")
    assert response.headers["Content-Type"] == "application/json"
    
    customer = response.json()
    assert isinstance(customer, dict)

    assert "id" in customer
    assert "first_name" in customer
    assert "last_name" in customer


def test_save_customer_status_code():
    customer = {
        "first_name": "Jane",
        "last_name": "Doe",
        "address": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA",
        "email": "jane.doe@example.com"
    }

    response = requests.post("http://127.0.0.1:5000/customers", json=customer)
    assert response.status_code == 200


def test_save_customer_retrieval():
    customer = {
        "first_name": "Jane",
        "last_name": "Doe",
        "address": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA",
        "email": "jane.doe@example.com"
    }

    response = requests.post("http://127.0.0.1:5000/customers", json=customer)
    customer_id = response.json()["id"]

    response = requests.get(f"http://127.0.0.1:5000/customers/{customer_id}")
    assert response.headers["Content-Type"] == "application/json"

    customer = response.json()
    assert isinstance(customer, dict)

    assert customer["id"] == customer_id
    assert customer["first_name"] == "Jane"
    assert customer["last_name"] == "Doe"
    assert customer["address"] == "123 Main Street"
    assert customer["city"] == "New York"
    assert customer["state"] == "NY"
    assert customer["postal_code"] == "10001"
    assert customer["country"] == "USA"
    assert customer["email"] == "jane.doe@example.com"


def test_update_customer_status_code():
    customer = {
        "first_name": "John",
        "last_name": "Smith",
    }

    create_response = requests.post("http://127.0.0.1:5000/customers", json=customer)
    customer_id = create_response.json()["id"]

    update_response = requests.post("http://127.0.0.1:5000/customers", json={"id": customer_id, "first_name": "David"})
    assert update_response.status_code == 200


def test_update_customer_retrieval():
    customer = {
        "first_name": "John",
        "last_name": "Smith",
        "address": "1234 Test St",
        "city": "Test City",
        "state": "Test State",
        "postal_code": "123456",
        "country": "Test Country",
        "email": "test@example.com"
    }

    create_response = requests.post("http://127.0.0.1:5000/customers", json=customer)
    customer_id = create_response.json()["id"]

    customer["first_name"] = "David"
    requests.post("http://127.0.0.1:5000/customers", json={"id": customer_id, **customer})
    
    get_response = requests.get(f"http://127.0.0.1:5000/customers/{customer_id}")
    assert get_response.headers["Content-Type"] == "application/json"
    
    customer = get_response.json()
    assert isinstance(customer, dict)

    assert customer["id"] == customer_id
    assert customer["first_name"] == "David"
    assert customer["last_name"] == "Smith"


def test_delete_customer_status_code():
    customer = {
        "first_name": "John",
        "last_name": "Smith",
        "address": "1234 Test St",
        "city": "Test City",
        "state": "Test State",
        "postal_code": "123456",
        "country": "Test Country",
        "email": "test@example.com"
    }

    create_response = requests.post("http://127.0.0.1:5000/customers", json=customer)
    customer_id = create_response.json()["id"]

    response = requests.delete(f"http://127.0.0.1:5000/customers/{customer_id}")
    assert response.status_code == 200

def test_delete_customer_retrieval():
    customer = {
        "first_name": "John",
        "last_name": "Smith",
        "address": "1234 Test St",
        "city": "Test City",
        "state": "Test State",
        "postal_code": "123456",
        "country": "Test Country",
        "email": "test@example.com"
    }

    create_response = requests.post("http://127.0.0.1:5000/customers", json=customer)
    customer_id = create_response.json()["id"]

    requests.delete(f"http://127.0.0.1:5000/customers/{customer_id}")

    response = requests.get(f"http://127.0.0.1:5000/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == None

###TEST SEARCH BY NAME
def test_search_customers_status_code():
    search = {
        "and_or": "and",
        "filters":[
            {
                "field": "first_name",
                "operator": "contains any",
                "value": "John"
            }
        ]
    }

    response = requests.post("http://127.0.0.1:5000/customers/search", json=search)
    assert response.status_code == 200


def test_search_customers_results():
    customer = {
        "first_name": "John",
        "last_name": "Smith",
        "address": "1234 Test St",
        "city": "Test City",
        "state": "Test State",
        "postal_code": "123456",
        "country": "Test Country",
        "email": "test@example.com"
    }

    requests.post("http://127.0.0.1:5000/customers", json=customer)

    search = {
        "and_or": "and",
        "filters": [
            {
                "field": "first_name",
                "operator": "contains any",
                "value": "John"
            }
        ]
    }

    response = requests.post("http://127.0.0.1:5000/customers/search", json=search)
    assert response.headers["Content-Type"] == "application/json"
    
    customers = response.json()
    assert isinstance(customers, list)

    for customer in customers:
        assert customer["first_name"] == "John"
        assert customer["last_name"] == "Smith"
