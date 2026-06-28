class Aeroplane:
    """Класс для представления информации о самолёте"""

    def __init__(
        self,
        icao24: str,
        callsign: str,
        origin_country: str,
        velocity: float,
        altitude: float,
    ):
        """
        Инициализация самолёта.

        Args:
            icao24: ICAO-адрес транспондера
            callsign: Позывной
            origin_country: Страна регистрации
            velocity: Скорость (м/с)
            altitude: Высота (м)
        """
        self.icao24 = icao24
        self.callsign = callsign.strip() if callsign else "Unknown"
        self.origin_country = origin_country
        self.velocity = self._validate_velocity(velocity)
        self.altitude = self._validate_altitude(altitude)

    @staticmethod
    def _validate_velocity(velocity: float) -> float:
        """Валидация скорости"""
        if velocity is None:
            return 0.0
        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        return round(velocity, 2)

    @staticmethod
    def _validate_altitude(altitude: float) -> float:
        """Валидация высоты"""
        if altitude is None:
            return 0.0
        if altitude < 0:
            raise ValueError("Высота не может быть отрицательной")
        return round(altitude, 2)

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение самолётов по скорости (для сортировки)"""
        return self.velocity < other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        return self.velocity > other.velocity

    def __eq__(self, other: "Aeroplane") -> bool:
        return self.icao24 == other.icao24

    def __str__(self):
        return f"{self.callsign} ({self.origin_country}): {self.velocity} м/с, {self.altitude} м"

    @classmethod
    def cast_to_object_list(cls, data: list) -> list["Aeroplane"]:
        """
        Преобразует сырые данные из API в список объектов Aeroplane.

        Args:
            data: Список состояний из OpenSky API

        Returns:
            Список объектов Aeroplane
        """
        aeroplanes = []
        for state in data:
            try:
                # Поля в OpenSky API:
                # 0: icao24, 1: callsign, 2: origin_country,
                # 4: longitude, 5: latitude, 6: altitude,
                # 7: on_ground, 9: velocity
                icao24 = state[0]
                callsign = state[1] if state[1] else "Unknown"
                origin_country = state[2] if state[2] else "Unknown"
                altitude = float(state[7]) if state[7] is not None else 0.0
                velocity = float(state[9]) if state[9] is not None else 0.0

                aeroplane = cls(icao24, callsign, origin_country, velocity, altitude)
                aeroplanes.append(aeroplane)
            except ValueError, IndexError, TypeError:
                continue

        return aeroplanes
