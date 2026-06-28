import pytest

from src.abstract_storage import AbstractStorage
from src.aeroplane import Aeroplane


class TestAbstractStorage:
    def test_cant_instantiate_abstract_class(self):
        """Нельзя создать объект абстрактного класса"""
        with pytest.raises(TypeError):
            AbstractStorage()

    def test_concrete_class_implements_methods(self):
        """Проверка, что класс-наследник реализует все методы"""

        class ConcreteStorage(AbstractStorage):
            def add_aeroplane(self, aeroplane: Aeroplane) -> None:
                pass

            def get_aeroplanes(self, **filters) -> list:
                return []

            def delete_aeroplane(self, icao24: str) -> bool:
                return False

            def load_data(self) -> list:
                return []

        # Создаём экземпляр, чтобы проверить, что методы реализованы
        storage = ConcreteStorage()
        assert isinstance(storage, AbstractStorage)
