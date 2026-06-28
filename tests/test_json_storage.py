import os
import tempfile

from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


class TestJSONStorage:
    def setup_method(self):
        """Создаём временный файл для тестов"""
        self.temp_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w", encoding="utf-8"
        )
        self.file_path = self.temp_file.name
        self.temp_file.close()
        self.storage = JSONStorage(self.file_path)

    def teardown_method(self):
        """Удаляем временный файл после теста"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_ensure_file_exists(self):
        storage = JSONStorage(self.file_path)
        assert storage.file_path == self.file_path
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content in ["", "[]"]

    def test_add_aeroplane(self):
        a = Aeroplane("abc123", "UAL1621", "US", 268.79, 10203.18)
        self.storage.add_aeroplane(a)

        data = self.storage._read_data()
        assert len(data) == 1
        assert data[0]["icao24"] == "abc123"
        assert data[0]["callsign"] == "UAL1621"

    def test_add_duplicate_aeroplane(self):
        a = Aeroplane("abc123", "UAL1621", "US", 268.79, 10203.18)
        self.storage.add_aeroplane(a)
        self.storage.add_aeroplane(a)

        data = self.storage._read_data()
        assert len(data) == 1

    def test_get_aeroplanes_all(self):
        a1 = Aeroplane("1", "A", "US", 100, 1000)
        a2 = Aeroplane("2", "B", "UK", 200, 2000)
        self.storage.add_aeroplane(a1)
        self.storage.add_aeroplane(a2)

        result = self.storage.get_aeroplanes()
        assert len(result) == 2

    def test_get_aeroplanes_filtered(self):
        a1 = Aeroplane("1", "A", "US", 100, 1000)
        a2 = Aeroplane("2", "B", "UK", 200, 2000)
        self.storage.add_aeroplane(a1)
        self.storage.add_aeroplane(a2)

        result = self.storage.get_aeroplanes(origin_country="UK")
        assert len(result) == 1
        assert result[0].icao24 == "2"

    def test_delete_aeroplane(self):
        a = Aeroplane("abc123", "UAL1621", "US", 268.79, 10203.18)
        self.storage.add_aeroplane(a)

        result = self.storage.delete_aeroplane("abc123")
        assert result is True

        data = self.storage._read_data()
        assert len(data) == 0

    def test_delete_aeroplane_not_found(self):
        result = self.storage.delete_aeroplane("nonexistent")
        assert result is False

    def test_load_data(self):
        a1 = Aeroplane("1", "A", "US", 100, 1000)
        a2 = Aeroplane("2", "B", "UK", 200, 2000)
        self.storage.add_aeroplane(a1)
        self.storage.add_aeroplane(a2)

        result = self.storage.load_data()
        assert len(result) == 2
        assert result[0].icao24 == "1"
        assert result[1].icao24 == "2"

    def test_read_data_invalid_json(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("{invalid json}")
        result = self.storage._read_data()
        assert result == []
