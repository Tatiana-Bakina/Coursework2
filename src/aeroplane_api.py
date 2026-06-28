import requests

from src.abstract_api import AbstractAeroplaneAPI


class AeroplaneAPI(AbstractAeroplaneAPI):
    """Класс для работы с API OpenSky и Nominatim"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def get_country_coordinates(self, country_name: str) -> dict:
        """
        Получает координаты страны через Nominatim API.
        """
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"q": country_name, "format": "json", "limit": 1}
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            if not data:
                raise ValueError(f"Страна '{country_name}' не найдена")

            boundingbox = data[0]["boundingbox"]
            return {
                "south": float(boundingbox[0]),
                "north": float(boundingbox[1]),
                "west": float(boundingbox[2]),
                "east": float(boundingbox[3]),
            }

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к Nominatim: {e}")
            raise
        except (KeyError, IndexError, ValueError) as e:
            print(f"Ошибка при обработке данных Nominatim: {e}")
            raise

    def get_aeroplanes(self, country_name: str) -> list:
        """
        Получает данные о самолётах через OpenSky API.
        """
        try:
            coords = self.get_country_coordinates(country_name)
            url = "https://opensky-network.org/api/states/all"
            params = {
                "lamin": coords["south"],
                "lamax": coords["north"],
                "lomin": coords["west"],
                "lomax": coords["east"],
            }
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("states", [])
        except Exception as e:  # ← ловим любое исключение
            print(f"Ошибка при запросе к OpenSky: {e}")
            return []
