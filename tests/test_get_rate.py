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
        response = get_current_rates()
        self.assertEqual(200,
                         response.status_code,
                         "Happy status code should come back 200")

        self.assertTrue(response.json(), "Happy response should have a body")
        self.assertTrue(response.json()["rates"], "Happy response should have rates")

    @patch('fixercise.get_rates.requests.get')
    def test_get_historical_rate_happy(self, mock_response):
        """Check "happy" historic rate call."""
        historic_date = datetime(2018, 1, 1)
        historic_iso_date = historic_date.strftime('%Y-%m-%d')
        mock_response.return_value = testutils.mock_api_response(200, when=historic_date)
        response = get_historic_rates(historic_iso_date)
        self.assertEqual(200,
                         response.status_code,
                         "Happy status code should come back 200")

        self.assertTrue(response.json(), "Happy response should have a body")
        self.assertTrue(response.json()["rates"], "Happy response should have rates")
        self.assertEqual(historic_iso_date, response.json()["date"],
                         "Happy response date should match request date")

    @patch('fixercise.get_rates.requests.get')
    def test_get_rates_bad_api_call(self, mock_response):
        pass

    @patch('fixercise.get_rates.requests.get')
    def test_get_rates_bad_status(self, mock_response):
        pass

if __name__ == '__main__':
    unittest.main()