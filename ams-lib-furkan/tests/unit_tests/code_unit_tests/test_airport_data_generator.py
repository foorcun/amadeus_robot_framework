from ams.data_model.common_libs.utils.airport_data_generator import GenerateAirportData
import string


def test_generate_airline_code():
    prefix = "AA"
    length = 4
    result = GenerateAirportData.generate_airline_code(prefix, length)
    assert result.startswith(prefix)
    assert len(result) == len(prefix) + length
    assert result[len(prefix) :].isdigit()


def test_generate_flight_number():
    length = 5
    result = GenerateAirportData.generate_flight_number(length)
    assert len(result) == length
    assert result.isdigit()


def test_generate_correlation_id():
    size = 50
    result = GenerateAirportData.generate_correlation_id(size)
    assert len(result) == size
    assert all(
        c in (string.ascii_uppercase + string.digits + string.ascii_lowercase)
        for c in result
    )


def test_generate_uuid():
    result = GenerateAirportData.generate_uuid()
    assert len(result) == 36
    assert isinstance(result, str)


def test_generate_airline_code_invalid_length():
    prefix = "AA"
    length = 0
    result = GenerateAirportData.generate_airline_code(prefix, length)
    assert result == prefix


def test_generate_flight_number_invalid_length():
    length = 0
    result = GenerateAirportData.generate_flight_number(length)
    assert result == ""


def test_generate_correlation_id_default_size():
    result = GenerateAirportData.generate_correlation_id()
    assert len(result) == 50
    assert all(
        c in (string.ascii_uppercase + string.digits + string.ascii_lowercase)
        for c in result
    )
