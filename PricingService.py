"""
Description:
Solution for https://github.com/QueensLabOpen/EvaluationAssignment/tree/master/Backend

Assumptions:
- No escaping since it's an internal api
- Trusted inputs, no need to validate
- Normally I would poll a database for discount, free days and start date + price for services on customer id
  Now however, I'm sending that data as input with POST instead of GET here for POC
- No end dates on services since it wasn't specified (interesting business approach)
- No data type enforcement
- No error handling
- Not adding full test coverage
- Looping over days to calculate price. Could be done algorithmically for better performance
"""

from flask import Flask, request
from scripts.PriceCalculator import calculate_price


app = Flask(__name__)

# ROUTES


@app.route("/")
def index():
    return "<p>Access api with /api</p>"


@app.route("/api", methods=["POST"])
def get_customer_price():
    data = request.json

    price = calculate_price(data)
    return_data = {"price": round(price, 2), "currency": "€"}

    return return_data


if __file__ == "__main__":
    print("Should not be run directly")
