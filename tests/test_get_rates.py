import unittest
from datetime import datetime
from unittest.mock import patch
from fixercise.get_rates import *

import tests.testutils as testutils


class TestGetRates(unittest.TestCase):

    @patch('fixercise.get_rates.requests.get')
    def test_get_rates_happy(self, mock_response):
        """Check a response with status 200 and body returns happily."""
        mock_response.return_value = testutils.mock_api_response(200)
        data = get_current_rates()

        self.assertTrue(data, "Happy response should have a body")
        self.assertTrue(data["rates"], "Happy response should have rates")

    @patch('fixercise.get_rates.requests.get')
    def test_get_historical_rate_happy(self, mock_response):
        """Check "happy" historic rate call."""
        historic_date = datetime(2018, 1, 1)
        historic_iso_date = historic_date.strftime('%Y-%m-%d')
        mock_response.return_value = testutils.mock_api_response(200, when=historic_date)
        data = get_historic_rates(historic_iso_date)

        self.assertTrue(data, "Happy response should have a body")
        self.assertTrue(data["rates"], "Happy response should have rates")
        self.assertEqual(historic_iso_date, data["date"],
                         "Happy response date should match request date")

    @patch('fixercise.get_rates.requests.get')
    def test_get_rates_bad_api_call(self, mock_response):

        # Get a mocked API response that reports as unsuccessful
        # but with a 200 status code on the web response
        mock_return_value = testutils.mock_api_response(200)
        mock_return_value.json_data["success"] = False
        mock_return_value.json_data["error"] = {
            "code": 999,
            "type": "Totally bogus error",
            "message": "This API error is made up"
        }
        mock_response.return_value = mock_return_value

        with self.assertRaises(BadCallException,
                               msg="Non-200 response should raise exception"):
            get_current_rates()

    @patch('fixercise.get_rates.requests.get')
    def test_get_rates_bad_status(self, mock_response):
        historic_date = datetime(2018, 1, 1)
        historic_iso_date = historic_date.strftime('%Y-%m-%d')
        mock_response.return_value = testutils.mock_api_response(500)

        with self.assertRaises(BadResponseException,
                               msg="Non-200 response should raise exception"):
            get_historic_rates(historic_iso_date)
