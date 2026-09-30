import allure
import pytest
from pydantic import ValidationError
from core.models.booking import BookingResponse


#Мой автотест из Урока 5 (Тесты на метод Ping):
@allure.feature("Test CreateBooking")
@allure.story("Test creating booking")
def test_create_booking(api_client, generate_random_booking_data):
    booking_payload = generate_random_booking_data
    with allure.step("Create booking"):
        response = api_client.create_booking(booking_payload)
        response_json = response.json()

    with allure.step("Verify response booking ID"):
        assert isinstance(response_json.get("bookingid"), int), "Invalid booking ID"



@allure.feature("Test creating booking")
@allure.story("Positive: creating booking with custom data")
def test_creating_booking_with_custom_data(api_client):
    booking_data = {
        "firstname" : "Ivan",
        "lastname" : "Ivanovich",
        "totalprice" : 150,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2025-02-01",
            "checkout" : "2025-02-18"
        },
    "additionalneeds" : "Dinner"
    }

    response = api_client.create_booking(booking_data)
    response_json = response.json()
    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response_json['booking']['firstname'] == booking_data['firstname']
    assert response_json['booking']['lastname'] == booking_data['lastname']
    assert response_json['booking']['totalprice'] == booking_data['totalprice']
    assert response_json['booking']['depositpaid'] == booking_data['depositpaid']
    assert response_json['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response_json['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response_json['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature("Test creating booking")
@allure.story("Positive: creating booking with random data")
def test_creating_booking_with_random_data(api_client, generate_random_booking_data):
    random_booking_data = generate_random_booking_data

    response = api_client.create_booking(random_booking_data)
    response_json = response.json()
    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response_json['booking']['firstname'] == random_booking_data['firstname']
    assert response_json['booking']['lastname'] == random_booking_data['lastname']
    assert response_json['booking']['totalprice'] == random_booking_data['totalprice']
    assert response_json['booking']['depositpaid'] == random_booking_data['depositpaid']
    assert response_json['booking']['bookingdates']['checkin'] == random_booking_data['bookingdates']['checkin']
    assert response_json['booking']['bookingdates']['checkout'] == random_booking_data['bookingdates']['checkout']
    assert response_json['booking']['additionalneeds'] == random_booking_data['additionalneeds']


@allure.feature("Test creating booking")
@allure.story("Negative: creating booking without required fields")
def test_creating_booking_without_required_fields(api_client, booking_dates):
    missing_fields = booking_dates
    response = api_client.create_booking(missing_fields, raise_for_status=False)

    with allure.step("Verify response status code"):
        assert response.status_code == 500, f"Expected status 500 but got {response.status_code}"


@allure.feature("Test creating booking")
@allure.story("Negative: invalid checkin data types")
@pytest.mark.xfail(reason="Ответ возвращает код 200", strict=False)
@pytest.mark.parametrize("bad_date", [
    "31-12-2025",
    "yesterday",
    1700000000,
    None
])

def test_creating_booking_with_invalid_date_type(api_client, generate_random_booking_data, bad_date):
    booking_data = generate_random_booking_data
    booking_data["bookingdates"] = {
        "checkin": bad_date,
        "checkout": "2025-12-31"
    }

    response = api_client.create_booking(booking_data, raise_for_status=False)
    with allure.step("Verify response status code"):
        assert response.status_code == 400, f"Expected status 400 but got {response.status_code}"


@allure.feature("Test creating booking")
@allure.story("Negative: checkout date before checkin date")
@pytest.mark.xfail(reason="Ответ возвращает код 200",strict=False,)
def test_creating_booking_checkout_before_checkin(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    booking_data["bookingdates"] = {
        "checkin": "2025-02-10",
        "checkout": "2025-02-01",
    }

    response = api_client.create_booking(booking_data, raise_for_status=False)
    with allure.step("Verify response status code"):
        assert (response.status_code == 400), f"Expected status 400 but got {response.status_code}"


@allure.feature("Test creating booking")
@allure.story("Negative: invalid firstname and lastname data types")
@pytest.mark.xfail(reason="Ответ возвращает код 200", strict=False)
@pytest.mark.parametrize("bad_types", [
    "31-12-2025",
    "yesterday",
    1700000000,
    None
])
def test_creating_booking_with_invalid_names_data_types(api_client, generate_random_booking_data, bad_types):
    booking_data = generate_random_booking_data
    booking_data["firstname"] = bad_types
    booking_data["lastname"] = bad_types

    response = api_client.create_booking(booking_data, raise_for_status=False)

    with allure.step("Verify response status code"):
        assert response.status_code == 400, f"Expected status 400 but got {response.status_code}"