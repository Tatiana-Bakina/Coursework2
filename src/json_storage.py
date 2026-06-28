import json
import os
from typing import List

from src.abstract_storage import AbstractStorage
from src.aeroplane import Aeroplane


class JSONStorage(AbstractStorage):
    """Класс для сохранения данных в JSON-файл"""

    def __init__(self, file_path: str = "data/aeroplanes.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создаёт файл, если он не существует"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_data(self) -> List[dict]:
        """Читает данные из JSON-файла"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError, FileNotFoundError:
            return []

    def _write_data(self, data: List[dict]) -> None:
        """Записывает данные в JSON-файл"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в JSON-файл"""
        data = self._read_data()

        # Проверяем, есть ли уже такой самолёт
        for item in data:
            if item.get("icao24") == aeroplane.icao24:
                return

        data.append(
            {
                "icao24": aeroplane.icao24,
                "callsign": aeroplane.callsign,
                "origin_country": aeroplane.origin_country,
                "velocity": aeroplane.velocity,
                "altitude": aeroplane.altitude,
            }
        )
        self._write_data(data)

    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        """Получает самолёты по фильтрам"""
        data = self._read_data()
        result = []

        for item in data:
            match = True
            for key, value in filters.items():
                if key in item and item[key] != value:
                    match = False
                    break
            if match:
                try:
                    aeroplane = Aeroplane(
                        item["icao24"],
                        item["callsign"],
                        item["origin_country"],
                        item["velocity"],
                        item["altitude"],
                    )
                    result.append(aeroplane)
                except KeyError, ValueError:
                    continue

        return result

    def delete_aeroplane(self, icao24: str) -> bool:
        """Удаляет самолёт по ICAO"""
        data = self._read_data()
        initial_len = len(data)

        new_data = [item for item in data if item.get("icao24") != icao24]
        if len(new_data) < initial_len:
            self._write_data(new_data)
            return True
        return False

    def load_data(self) -> List[Aeroplane]:
        """Загружает все данные из JSON-файла"""
        return self.get_aeroplanes()
