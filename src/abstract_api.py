from abc import ABC, abstractmethod


class AbstractAeroplaneAPI(ABC):
    """Абстрактный класс для работы с API самолётов"""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> dict:
        """
        Получает географические координаты страны по её названию.

        Args:
            country_name: Название страны (например, "Russia", "Spain")

        Returns:
            Словарь с координатами:
            {
                "south": float,  # южная широта
                "north": float,  # северная широта
                "west": float,   # западная долгота
                "east": float    # восточная долгота
            }

        Raises:
            ValueError: Если страна не найдена
            requests.exceptions.RequestException: При ошибке запроса
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> list:
        """
        Получает информацию о самолётах в воздушном пространстве страны.

        Args:
            country_name: Название страны

        Returns:
            Список состояний самолётов (сырые данные из OpenSky API)

        Raises:
            requests.exceptions.RequestException: При ошибке запроса
        """
        pass
