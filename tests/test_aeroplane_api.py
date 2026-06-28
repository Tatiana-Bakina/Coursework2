from unittest.mock import Mock, patch

import pytest

from src.aeroplane_api import AeroplaneAPI


class TestAeroplaneAPI:
    @patch("src.aeroplane_api.requests.get")
    def test_get_country_coordinates_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"boundingbox": ["40.0", "50.0", "20.0", "30.0"]}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = AeroplaneAPI()
        result = api.get_country_coordinates("Spain")

        assert result["south"] == 40.0
        assert result["north"] == 50.0
        assert result["west"] == 20.0
        assert result["east"] == 30.0

    @patch("src.aeroplane_api.requests.get")
    def test_get_country_coordinates_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = AeroplaneAPI()
        with pytest.raises(ValueError, match="Страна 'InvalidCountry' не найдена"):
            api.get_country_coordinates("InvalidCountry")

    @patch("src.aeroplane_api.requests.get")
    def test_get_aeroplanes_success(self, mock_get):
        # Первый запрос — Nominatim
        mock_country_response = Mock()
        mock_country_response.json.return_value = [
            {"boundingbox": ["40.0", "50.0", "20.0", "30.0"]}
        ]
        mock_country_response.raise_for_status = Mock()

        # Второй запрос — OpenSky
        mock_opensky_response = Mock()
        mock_opensky_response.json.return_value = {
            "states": [
                [
                    "abc123",
                    "UAL1621",
                    "US",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    268.79,
                    None,
                    None,
                ]
            ]
        }
        mock_opensky_response.raise_for_status = Mock()

        mock_get.side_effect = [mock_country_response, mock_opensky_response]

        api = AeroplaneAPI()
        result = api.get_aeroplanes("Spain")

        assert len(result) == 1
        assert result[0][0] == "abc123"

    @patch("src.aeroplane_api.requests.get")
    def test_get_aeroplanes_api_error(self, mock_get):
        """Тест: ошибка при запросе к API"""
        mock_get.side_effect = Exception("Connection error")

        api = AeroplaneAPI()
        result = api.get_aeroplanes("Spain")
        assert result == []

    @patch("src.aeroplane_api.requests.get")
    def test_get_country_coordinates_request_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        api = AeroplaneAPI()
        with pytest.raises(Exception, match="Network error"):
            api.get_country_coordinates("Spain")
