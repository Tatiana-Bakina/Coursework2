import pytest

from src.aeroplane import Aeroplane


class TestAeroplane:
    def test_initialization(self):
        a = Aeroplane("abc123", "UAL1621", "United States", 268.79, 10203.18)
        assert a.icao24 == "abc123"
        assert a.callsign == "UAL1621"
        assert a.origin_country == "United States"
        assert a.velocity == 268.79
        assert a.altitude == 10203.18

    def test_callsign_strip(self):
        a = Aeroplane("abc123", "  UAL1621  ", "US", 100, 1000)
        assert a.callsign == "UAL1621"

    def test_callsign_default(self):
        a = Aeroplane("abc123", None, "US", 100, 1000)
        assert a.callsign == "Unknown"

    def test_origin_country_default(self):
        a = Aeroplane("abc123", "A", "", 100, 1000)
        assert a.origin_country == ""

    def test_validation_negative_velocity(self):
        with pytest.raises(ValueError, match="Скорость не может быть отрицательной"):
            Aeroplane("abc123", "UAL1621", "US", -100, 1000)

    def test_validation_negative_altitude(self):
        with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
            Aeroplane("abc123", "UAL1621", "US", 100, -500)

    def test_validation_zero_velocity(self):
        a = Aeroplane("abc123", "A", "US", 0, 1000)
        assert a.velocity == 0.0

    def test_none_values(self):
        a = Aeroplane("abc123", "A", "US", None, None)
        assert a.velocity == 0.0
        assert a.altitude == 0.0

    def test_comparison_lt(self):
        a1 = Aeroplane("1", "A", "US", 100, 1000)
        a2 = Aeroplane("2", "B", "US", 200, 2000)
        assert a1 < a2

    def test_comparison_gt(self):
        a1 = Aeroplane("1", "A", "US", 300, 1000)
        a2 = Aeroplane("2", "B", "US", 200, 2000)
        assert a1 > a2

    def test_comparison_eq(self):
        a1 = Aeroplane("abc123", "A", "US", 100, 1000)
        a2 = Aeroplane("abc123", "B", "US", 200, 2000)
        assert a1 == a2

    def test_comparison_ne(self):
        a1 = Aeroplane("abc123", "A", "US", 100, 1000)
        a2 = Aeroplane("def456", "B", "US", 200, 2000)
        assert a1 != a2

    def test_str(self):
        a = Aeroplane("abc123", "UAL1621", "United States", 268.79, 10203.18)
        expected = "UAL1621 (United States): 268.79 м/с, 10203.18 м"
        assert str(a) == expected

    def test_cast_to_object_list(self):
        data = [
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
            ],
            [
                "def456",
                "BAW123",
                "UK",
                None,
                None,
                None,
                None,
                None,
                None,
                150.0,
                None,
                None,
            ],
        ]
        result = Aeroplane.cast_to_object_list(data)
        assert len(result) == 2
        assert result[0].icao24 == "abc123"
        assert result[0].velocity == 268.79
        assert result[1].icao24 == "def456"

    def test_cast_to_object_list_invalid(self):
        data = [
            ["abc123", "A", "US", None, None, None, None, None, None, 100, None, None],
            ["invalid"],  # неполные данные
            ["def456", "B", "UK", None, None, None, None, None, None, 200, None, None],
        ]
        result = Aeroplane.cast_to_object_list(data)
        # invalid пропускается, остальные 2 обрабатываются
        assert len(result) == 2
