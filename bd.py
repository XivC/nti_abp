"""
	Вся работа с БД будет тут
"""
import sqlite3


class BD:
	def __init__(self, name_bd):
		""" инитиализация курсора и бд"""
		self.conn = sqlite3.connect(name_bd)
		self.cursor = self.conn.cursor()

	def create_tables(self):
		""" Creating new base of date"""
		self.cursor.execute("""
			CREATE TABLE details
			(id, name_detail, type)
			""")
		self.cursor.execute("""
						CREATE TABLE drons
					(id, name_dron, cost)
				""")
		self.cursor.execute("""
					CREATE TABLE dron_map
					(id, name, detail, count_detail)
				""")
		self.conn.commit()
		return True

	def insert_in_tables(self, details_table, drons_table, dron_map):
		print("inserting in data")
		# Добавляет в таблицы данные


	def