"""
	Главный файл, тут будет все запускные механизмы и т.д.
"""
import bd
import front

bdd = bd.BD()
bdd.create_tables() # Создание базы данных

if __name__ == "__main__":
	front.mainWindow()
