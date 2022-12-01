"""
Calculates prices used in PricingService.py
"""

from .Constants import BASE_COSTS, SERVICE_DAY_COST
import datetime


def calculate_price(data):
    """
    Returns price for a specified period of time for a customer taking individual prices, services,
    discounts and free days into account

    :param dict data: Data including start and end date as well as customer data e.g. service discounts
    :returns:  The price for a customer for a specified period of time
    :rtype: float
    """
    cost_per_service = {}
    free_days_left = data["free_days"]

    # Convert dates from type string to type date
    start_date = string_to_date(data["start_date"])
    end_date = string_to_date(data["end_date"])
    service_start_dates = {
        service: string_to_date(date)
        for service, date in data["service_start"].items()
    }

    # Loop over days
    n_days = (end_date - start_date).days + 1  # Include last day
    i_date = start_date
    for _ in range(n_days):
        # Loop over services
        for service, service_start_date in service_start_dates.items():
            # Does service have a start date
            if not service_start_date:
                continue

            # Check if service costs anything this day of the week
            if current_weekday(i_date) not in SERVICE_DAY_COST[service]:
                continue

            # Check if service has started
            if service_start_date <= i_date:
                # Consume free days first
                if free_days_left > 0:
                    free_days_left -= 1
                    break

                # Calculate cost for service that day and apply potential discount
                service_price = calculate_service_price(
                    service, data["service_price"])
                service_discount = get_service_discount(
                    i_date, data["discount"][service])
                service_cost = service_price * (1 - service_discount)

                # Add cost to service
                cost_per_service[service] = cost_per_service.get(
                    service, 0) + service_cost

        # Increment day
        i_date += datetime.timedelta(days=1)

    # Sum cost of services
    total_cost = sum(cost_per_service.values())

    return total_cost


def calculate_service_price(service, customer_price):
    """
    Returns price per day for a service for a customer

    :param str service: The service
    :param dict customer_price: Customer price per service
    :returns:  The price
    :rtype: float
    """
    if customer_price[service]:
        price = customer_price[service]
    else:
        price = BASE_COSTS[service]
    return price


def get_service_discount(current_date, discount):
    """
    Returns discount if current date has a discount. Else 0

    :param date current_date: Evaluated date
    :param dict discount: Amount, start date and en date of discount
    :returns:  The discount
    :rtype: float
    """
    if not discount["amount"]:
        return float(0)

    # Convert dates. Use "infinite" range if none is provided
    if discount["start_date"]:
        start_date = string_to_date(discount["start_date"])
    else:
        start_date = string_to_date("1970-01-01")

    if discount["end_date"]:
        end_date = string_to_date(discount["end_date"])
    else:
        end_date = string_to_date("2999-01-01")

    # Return discount if current date has a discount
    if start_date <= current_date <= end_date:
        return float(discount["amount"])

    return float(0)


def string_to_date(s):
    """
    Converts a date with type string to to date.
    Returns None if input is None

    :param str s: A date with format YYYY-MM-DD
    :returns:  The date | None
    :rtype: datetime.date | None
    """
    if s is None:
        return s
    s_list = s.split("-")
    s_list = map(int, s_list)
    return datetime.date(*s_list)


def current_weekday(date):
    """
    Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.

    :param date d: A date
    :returns:  Weekday
    :rtype: int
    """
    return int(date.strftime('%w'))
