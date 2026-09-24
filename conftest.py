import pytest
from core.clients.api_client import APIClient
from datetime import datetime, timedelta
from faker import Faker


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture()
def booking_dates():
    today = datetime.today()
    checkin = today + timedelta(days=5)
    checkout = today + timedelta(days=10)

    return {
        "checkin": checkin.strftime("%Y-%m-%d"),
        "checkout": checkout.strftime("%Y-%m-%d"),
    }


@pytest.fixture()
def generate_random_booking_date(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds,
    }

    return data