from unittest.mock import patch
from src.user_interface import user_interaction


class TestUserInteraction:
    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_get_aeroplanes_by_country(self, mock_storage, mock_api):
        mock_api_instance = mock_api.return_value
        mock_api_instance.get_aeroplanes.return_value = [
            ["abc123", "UAL1621", "US", None, None, None, None, None, None, 268.79, None, None]
        ]

        with patch("builtins.input", side_effect=["1", "Spain", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_api_instance.get_aeroplanes.assert_called_with("Spain")

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_save_aeroplanes(self, mock_storage, mock_api):
        mock_api_instance = mock_api.return_value
        mock_api_instance.get_aeroplanes.return_value = [
            ["abc123", "UAL1621", "US", None, None, None, None, None, None, 268.79, None, None]
        ]

        with patch("builtins.input", side_effect=["1", "Spain", "4", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_storage.return_value.add_aeroplane.assert_called()

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_top_n_altitude(self, mock_storage, mock_api):
        mock_api_instance = mock_api.return_value
        mock_api_instance.get_aeroplanes.return_value = [
            ["abc123", "A", "US", None, None, None, None, None, 1000, 100, None, None],
            ["def456", "B", "UK", None, None, None, None, None, 2000, 200, None, None],
            ["ghi789", "C", "FR", None, None, None, None, None, 1500, 150, None, None],
        ]

        with patch("builtins.input", side_effect=["1", "Spain", "2", "2", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_api_instance.get_aeroplanes.assert_called_with("Spain")

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_load_from_json(self, mock_storage, mock_api):
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.load_data.return_value = []

        with patch("builtins.input", side_effect=["5", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_storage_instance.load_data.assert_called()

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_filter_by_country(self, mock_storage, mock_api):
        mock_api_instance = mock_api.return_value
        mock_api_instance.get_aeroplanes.return_value = [
            ["abc123", "A", "United States", None, None, None, None, None, None, 100, None, None],
            ["def456", "B", "France", None, None, None, None, None, None, 200, None, None],
            ["ghi789", "C", "United States", None, None, None, None, None, None, 150, None, None],
        ]

        with patch("builtins.input", side_effect=["1", "Spain", "3", "United States", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_api_instance.get_aeroplanes.assert_called()

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_filter_no_data(self, mock_storage, mock_api):
        mock_api_instance = mock_api.return_value
        mock_api_instance.get_aeroplanes.return_value = [
            ["abc123", "A", "United States", None, None, None, None, None, None, 100, None, None],
        ]

        with patch("builtins.input", side_effect=["1", "Spain", "3", "Germany", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_api_instance.get_aeroplanes.assert_called()

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_save_without_data(self, mock_storage, mock_api):
        mock_api_instance = mock_api.return_value
        mock_api_instance.get_aeroplanes.return_value = []

        with patch("builtins.input", side_effect=["1", "Spain", "4", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_storage.return_value.add_aeroplane.assert_not_called()

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_top_n_without_data(self, mock_storage, mock_api):
        mock_api_instance = mock_api.return_value
        mock_api_instance.get_aeroplanes.return_value = []

        with patch("builtins.input", side_effect=["1", "Spain", "2", "5", "0"]):
            with patch("builtins.print"):
                user_interaction()
                mock_api_instance.get_aeroplanes.assert_called()

    @patch("src.user_interface.AeroplaneAPI")
    @patch("src.user_interface.JSONStorage")
    def test_invalid_choice(self, mock_storage, mock_api):
        with patch("builtins.input", side_effect=["99", "0"]):
            with patch("builtins.print") as mock_print:
                user_interaction()
                mock_print.assert_any_call("Неверный выбор, попробуйте снова")
