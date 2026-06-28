from src.aeroplane import Aeroplane
from src.aeroplane_api import AeroplaneAPI
from src.json_storage import JSONStorage


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем"""
    api = AeroplaneAPI()
    storage = JSONStorage()
    aeroplanes = []

    while True:
        print("\n" + "=" * 50)
        print("1. Получить информацию о самолётах по стране")
        print("2. Показать топ N самолётов по высоте")
        print("3. Фильтровать самолёты по стране регистрации")
        print("4. Сохранить текущие данные в JSON")
        print("5. Загрузить данные из JSON")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите действие: ")

        if choice == "0":
            print("До свидания!")
            break

        elif choice == "1":
            country = input("Введите название страны: ")
            try:
                raw_data = api.get_aeroplanes(country)
                aeroplanes = Aeroplane.cast_to_object_list(raw_data)
                print(
                    f"Найдено {len(aeroplanes)} самолётов в воздушном пространстве {country}"
                )
                for a in aeroplanes[:5]:  # показываем первые 5
                    print(f"  {a}")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            if not aeroplanes:
                print("Сначала получите данные о самолётах (пункт 1)")
                continue

            try:
                top_n = int(input("Введите количество самолётов для топа: "))
                sorted_aeroplanes = sorted(
                    aeroplanes, key=lambda x: x.altitude, reverse=True
                )
                top = sorted_aeroplanes[:top_n]

                print(f"\nТоп {top_n} самолётов по высоте:")
                for i, a in enumerate(top, 1):
                    print(f"{i}. {a.callsign} ({a.origin_country}) - {a.altitude} м")
            except ValueError:
                print("Введите корректное число")

        elif choice == "3":
            if not aeroplanes:
                print("Сначала получите данные о самолётах (пункт 1)")
                continue

            print(
                "Вводите страны на английском (например: Russia, United States, France)"
            )
            countries = input("Введите страны для фильтрации через запятую: ").split(
                ","
            )
            countries = [c.strip() for c in countries]

            filtered = [a for a in aeroplanes if a.origin_country in countries]

            print(f"Найдено {len(filtered)} самолётов")
            for a in filtered:
                print(f"  {a}")

        elif choice == "4":
            if not aeroplanes:
                print("Нет данных для сохранения")
                continue

            for a in aeroplanes:
                storage.add_aeroplane(a)
            print(f"Сохранено {len(aeroplanes)} самолётов в JSON")

        elif choice == "5":
            loaded = storage.load_data()
            print(f"Загружено {len(loaded)} самолётов из JSON")
            for a in loaded[:5]:
                print(f"  {a}")

        else:
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    user_interaction()
