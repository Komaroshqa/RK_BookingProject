import allure


@allure.feature("Test CreateBooking")
@allure.story("Test creating booking")
def test_create_booking(api_client, generate_random_booking_data):
    booking_payload = generate_random_booking_data
    with allure.step("Create booking"):
        response_json = api_client.create_booking(booking_payload)

    with allure.step("Verify response booking ID"):
        assert isinstance(response_json.get("bookingid"), int), "Invalid booking ID"

    with allure.step("Verify response payload matches creation data"):
        assert (response_json.get("booking") == booking_payload), f"Booking data mismatch with payload: {booking_payload}"