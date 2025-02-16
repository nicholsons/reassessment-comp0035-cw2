import pathlib

import pytest

from traffic import trafficdata


def test_simple():
    """
    This is a simple test that checks if the say_hello function returns the expected message.

    This is NOT a good example of a test. Do not use this as a template for writing your own tests!
    """
    result = trafficdata.say_hello()
    assert result == "Hello world"


def test_example():
    """
    This example test checks the get_rows method of the TrafficData class

    You may need to modify the db_path variable to point to the correct location of the traffic.db file in your project.

    Expected result: The number of rows returned should be 75
    """
    db_path = pathlib.Path(__file__).parent.parent.joinpath("src", "traffic", "traffic.db").resolve()
    print(f"Database path: {db_path}")
    traffic_data = trafficdata.TrafficData(db_path)
    result = traffic_data.get_rows("years")
    assert len(result) == 75


if __name__ == '__main__':
    # Run pytest tests/test_trafficdata.py
    pytest.main(['-v', __file__])
