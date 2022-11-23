import copy
import requests
import json
from scripts.Constants import test_base_dict, BASE_COSTS


URL = "http://127.0.0.1:5000/api"
HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}


def test_case_1_customer_x():
    """
    Customer X started using Service A and Service C 2019-09-20. Customer X also had an discount of 20% 
    between 2019-09-22 and 2019-09-24 for Service C. What is the total price for Customer X up until 2019-10-01?
    """
    # Setup test data
    test_input = copy.deepcopy(test_base_dict)
    test_input["service_start"]["serviceA"] = "2019-09-20"
    test_input["service_start"]["serviceC"] = "2019-09-20"
    test_input["discount"]["serviceC"] = {
        "amount": 0.2,
        "start_date": "2019-09-22",
        "end_date": "2019-09-24"
    }
    test_input["start_date"] = "2019-09-20"
    test_input["end_date"] = "2019-10-01"

    # Make request with test data
    data = json.dumps(test_input)
    res = requests.request(method="post", url=URL, data=data, headers=HEADERS)

    # Check output
    output = res.json()
    print(f'Test case 1: {output["currency"]} {output["price"]}')
    assert output["price"] == 6.16


def test_case_2_customer_y():
    """
    Customer Y started using Service B and Service C 2018-01-01. Customer Y had 200 free days 
    and a discount of 30% for the rest of the time. What is the total price for Customer Y up until 2019-10-01?
    """
    # Setup test data
    test_input = copy.deepcopy(test_base_dict)
    test_input["service_start"]["serviceB"] = "2018-01-01"
    test_input["service_start"]["serviceC"] = "2018-01-01"
    test_input["discount"]["serviceB"] = {
        "amount": 0.3,
        "start_date": None,
        "end_date": None,
    }
    test_input["discount"]["serviceC"] = test_input["discount"]["serviceB"].copy()
    test_input["start_date"] = "2018-01-01"
    test_input["end_date"] = "2019-10-01"
    test_input["free_days"] = 200

    # Make request with test data
    data = json.dumps(test_input)
    res = requests.request(method="post", url=URL, data=data, headers=HEADERS)

    # Check output
    output = res.json()
    print(f'Test case 2: {output["currency"]} {output["price"]}')
    assert output["price"] == 175.5  # rounded from 175.504


def test_case_3_infinite_free_days():
    """
    More free days than range
    """
    # Setup test data
    test_input = copy.deepcopy(test_base_dict)
    test_input["service_start"]["serviceA"] = "2018-01-01"
    test_input["service_start"]["serviceB"] = "2018-01-01"
    test_input["service_start"]["serviceC"] = "2018-01-01"
    test_input["start_date"] = "2018-01-01"
    test_input["end_date"] = "2019-10-01"
    test_input["free_days"] = 1000

    # Make request with test data
    data = json.dumps(test_input)
    res = requests.request(method="post", url=URL, data=data, headers=HEADERS)

    # Check output
    output = res.json()
    print(f'Test case 3: {output["currency"]} {output["price"]}')
    assert output["price"] == 0


def test_case_4_free_day_usage():
    """
    Free days should only count when services are active
    """
    # Setup test data
    test_input = copy.deepcopy(test_base_dict)
    test_input["service_start"]["serviceA"] = "2018-01-06"  # A saturday
    test_input["service_start"]["serviceB"] = "2018-01-07"
    test_input["service_start"]["serviceC"] = "2018-01-09"
    test_input["start_date"] = "2018-01-01"
    test_input["end_date"] = "2018-01-09"
    test_input["free_days"] = 1

    # Make request with test data
    data = json.dumps(test_input)
    res = requests.request(method="post", url=URL, data=data, headers=HEADERS)

    # Check output
    output = res.json()
    print(f'Test case 4: {output["currency"]} {output["price"]}')
    assert output["price"] == round(
        BASE_COSTS["serviceA"] + BASE_COSTS["serviceB"] + BASE_COSTS["serviceC"], 2)


def test_case_5_custom_prices():
    """
    Use custom prices and discounts
    """
    # Setup test data
    test_input = copy.deepcopy(test_base_dict)
    test_input["service_start"]["serviceA"] = "2018-01-01"
    test_input["service_start"]["serviceB"] = "2018-01-01"
    test_input["service_start"]["serviceC"] = "2018-01-01"
    test_input["service_price"]["serviceA"] = 0.1
    test_input["service_price"]["serviceB"] = 0.35
    test_input["service_price"]["serviceC"] = 0.65
    test_input["discount"]["serviceA"] = {
        "amount": 0.1,
        "start_date": None,
        "end_date": None,
    }
    test_input["discount"]["serviceB"] = {
        "amount": 0.05,
        "start_date": None,
        "end_date": None,
    }
    test_input["discount"]["serviceC"] = {
        "amount": 0.15,
        "start_date": None,
        "end_date": None,
    }
    test_input["start_date"] = "2018-01-03"  # Wedneseday
    test_input["end_date"] = "2018-01-07"  # Sunday

    # Make request with test data
    data = json.dumps(test_input)
    res = requests.request(method="post", url=URL, data=data, headers=HEADERS)

    # Check output
    output = res.json()
    print(f'Test case 5: {output["currency"]} {output["price"]}')

    serviceA = 3 * 0.1 * (1 - 0.1)
    serviceB = 3 * 0.35 * (1 - 0.05)
    serviceC = 5 * 0.65 * (1 - 0.15)
    assert output["price"] == round(serviceA + serviceB + serviceC, 2)


# Run tests
print("\n"*5)
test_case_1_customer_x()
test_case_2_customer_y()
test_case_3_infinite_free_days()
test_case_4_free_day_usage()
test_case_5_custom_prices()
