"""
	Главный файл, тут будет все запускные механизмы и т.д.
"""
import bd


def main():
	BD = bd.BD("cursor", "BASE")
	BD.create_bd() # Создание базы данных
	return 0;


if __name__ == "__main__":
	main()
