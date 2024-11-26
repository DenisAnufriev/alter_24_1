import requests
import stripe
from forex_python.converter import CurrencyRates
from rest_framework import status

from config.settings import CUR_API_KEY, STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """ Конвертирует рубли в доллары. """
    usd_price = 90
    response = requests.get(
        f"https://api.currencyapi.com/v3/latest?apikey={CUR_API_KEY}&currencies=RUB"
    )
    if response.status_code == status.HTTP_200_OK:
        usd_price = amount / response.json()["data"]["RUB"]["value"]
    return int(usd_price)


def create_stripe_price(amount):
    """
    Создаёт цену в страйпе.
    :param amount:
    :return:
    """
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Donation"},
    )


def create_stripe_session(price):
    """ Создаёт сессию на оплату в страйпе. """
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
