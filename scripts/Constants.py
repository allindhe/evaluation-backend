"""
Constants for pricing service as well as base case for test input
"""

# CONSTANTS
BASE_COSTS = {
    "serviceA": 0.2,
    "serviceB": 0.24,
    "serviceC": 0.4
}

SERVICE_DAY_COST = {
    "serviceA": [1, 2, 3, 4, 5],  # mon-fri
    "serviceB": [1, 2, 3, 4, 5],  # mon-fri
    "serviceC": [0, 1, 2, 3, 4, 5, 6]  # mon-sun
}

# Base case for testing
test_base_dict = {
    "id": 1,  # Customer id not used since no database is implemented
    "start_date": "1970-01-01",
    "end_date": "1970-01-01",
    "service_start": {
        "serviceA": None,
        "serviceB": None,
        "serviceC": None
    },
    "service_price": {
        "serviceA": None,
        "serviceB": None,
        "serviceC": None
    },
    "discount": {
        "serviceA": {
            "amount": None,
            "start_date": None,
            "end_date": None
        },
        "serviceB": {
            "amount": None,
            "start_date": None,
            "end_date": None
        },
        "serviceC": {
            "amount": None,
            "start_date": None,
            "end_date": None
        }
    },
    "free_days": 0
}
