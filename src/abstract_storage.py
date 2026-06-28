from abc import ABC, abstractmethod
from typing import List

from src.aeroplane import Aeroplane


class AbstractStorage(ABC):
    """Абстрактный класс для хранения информации о самолётах"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавляет информацию о самолёте в хранилище.

        Args:
            aeroplane: Объект самолёта для сохранения
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        """
        Получает список самолётов по заданным фильтрам.

        Args:
            **filters: Ключевые слова для фильтрации
                Например: origin_country="Russia", altitude=10000

        Returns:
            Список объектов Aeroplane, соответствующих фильтрам
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, icao24: str) -> bool:
        """
        Удаляет самолёт по его ICAO-адресу.

        Args:
            icao24: Уникальный ICAO-адрес транспондера

        Returns:
            True если самолёт был найден и удалён, иначе False
        """
        pass

    @abstractmethod
    def load_data(self) -> List[Aeroplane]:
        """
        Загружает все данные из хранилища.

        Returns:
            Список всех объектов Aeroplane из хранилища
        """
        pass
