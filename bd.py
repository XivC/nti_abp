import sqlite3


class BD:
	def __init__(self, name_bd="mybd.sqlite"):
		""" инитиализация курсора и бд"""
		self.conn = sqlite3.connect(name_bd)
		self.cursor = self.conn.cursor()
		self.filter = Filter()

	def create_tables(self):
		""" Creating new base of date"""
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS details 
			(id, name_detail, type)
			""")
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS drons
			(id, name_dron, cost)
			""")
		self.cursor.execute("""
			CREATE TABLE  IF NOT EXISTS dron_map
			(id, name, detail, count_detail)
			""")
		self.conn.commit()

		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS count_details
			(id, count)
			""")
		self.conn.commit()

		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS count_engins
			(id, serial_number)
		""")
		self.conn.commit()

		return True

	def insert_in_tables(self, details_table=[], drons_table=[], dron_map=[]):
		details_table, list_of_traces1 = self.filter.filter_details_table(details_table)
		self.cursor.executemany("INSERT INTO details VALUES (?,?,?)", details_table)
		self.conn.commit()
		
		drons_table, list_of_traces2 = self.filter.filter_details_table(drons_table)
		self.cursor.executemany("INSERT INTO drons VALUES (?,?,?)", drons_table)
		self.conn.commit()

		dron_map, list_of_traces3 = self.filter.filter_details_table(dron_map)
		self.cursor.executemany("INSERT INTO dron_map VALUES (?,?,?,?)", dron_map)
		self.conn.commit()
		
		return list_of_traces1 + list_of_traces3 + list_of_traces2

	def is_detail(self, name_detail):
		"""Возвращает деталь ли это"""
		self.cursor.execute('SELECT count(*) FROM details WHERE name_detail = ?', (name_detail,))
		data = self.cursor.fetchone()[0]
		return data > 0

	def is_engine(self, name_engine):
		"""Возвращает двигатель это или нет?"""
		# TODO me
		self.cursor.execute('SELECT type FROM details WHERE name_detail = ?', (name_engine,))
		data = self.cursor.fetchone()[0]
		return data == 'Аккумуляторные батареи' or data == 'batter'

	def give_all_details(self):
		"""Возвращает список всех деталий"""
		self.cursor.execute('SELECT* FROM "main"."details"')
		return self.cursor.fetchall()

	def write_in_bd(self, sl):
		"""принимает на вход словарь. И записывает его в бд
			sl = {
				'detail1': ['adarrea233', 1], # Это двигатель
				'detail2': ['', 123]          # Это не двигатель
			}
		"""
		return True


class Filter:

	def is_digit(self, string):
		if not str(string).isdigit():
			return (True, "строка {} не записана в {} базу данных, так как содержится буква в числе")
		return (False, "Все хорошо")

	def filter_details_table(self, details_table):
		"""
		фильтрует детали для бд
		:param details_table:
		:return: ([list for table], [лист ошибок почему вида : строка 23 не записана в бд,
																так как содержится буква в числе])
		"""
		list_of_traces = []
		index_line = 0
		filtered_detail_table = []
		for detail in details_table:
			flag, string = self.is_digit(detail[0])
			index_line += 1
			if flag:
				list_of_traces.append(string.format(index_line, "Таблице деталей"))
				continue
			filtered_detail_table.append(detail)
		return (filtered_detail_table, list_of_traces)

	def filter_drons_table(self, drons_table):
		"""
			фильтрует drons для бд
			:param drons_table:
			:return: ([list for table], [лист ошибок почему вида : строка 23 не записана в бд,
																		так как содержится буква в числе])
		"""
		list_of_traces = []
		index_line = 0
		filtered_drons_table = []
		for dron in drons_table:
			flag1, string1 = self.is_digit(dron[0])
			flag2, string2 = self.is_digit(dron[2])
			index_line += 1
			if flag1 or flag2:
				if flag1:
					list_of_traces.append(string1.format(index_line, 'Таблице дронов'))
				else:
					list_of_traces.append(string2.format(index_line, "Таблице дронов"))
				continue
			filtered_drons_table.append(dron)
		return (filtered_drons_table, list_of_traces)

	def filter_dron_map(self, dron_map):
		"""
			фильтрует детали для бд
			:param dron_map:
			:return: ([list for table], [лист ошибок почему вида : строка 23 не записана в бд,
																		так как содержится буква в числе])
		"""
		list_of_traces = []
		index_line = 0
		filtered_dron_map_table = []
		for dron in dron_map:	
			flag1, string1 = self.is_digit(dron[1])
			flag2, string2 = self.is_digit(dron[3])
			index_line += 1
			if flag1 or flag2:
				if flag1:
					list_of_traces.append(string1.format(index_line, "Технологические карты"))
				else:
					list_of_traces.append(string2.format(index_line, "Технологические карты"))
				continue
			filtered_dron_map_table.append(dron)
		return (filtered_dron_map_table, list_of_traces)


class Test:

	def __init__(self):
		self.bd = BD("TestBD.sqlite")
		self.bd.create_tables()

	def test_bd(self):
		# Тестовые данные
		details_table = [
			[1, 'detail1', 'batter'],
			[2, 'detail2', 'batter'],
			[3, 'detail3', 'other']
		]
		drons_table = [
			[1, 'dron1', 100],
			[2, 'dron2', 300]
		]
		dron_map = [
			[1, 'dron1', 'detail1', 23],
			[1, 'dron1', 'detail2', 2],
			[2, 'dron2', 'detail1', 1],
			[2, 'dron2', 'detail2', 345]
		]
		self.bd.insert_in_tables(drons_table=drons_table,
						dron_map=dron_map,
						details_table=details_table)

	def test_give_all_details(self):
		print("test_give_all_details")
		print(self.bd.give_all_details())

	def test_is_engine(self):
		print('detail1 is engine', self.bd.is_engine('detail1'))
		print('detail3 is engine', self.bd.is_engine('detail3'))

	def test_is_detail(self):
		print('is detail1', self.bd.is_detail('detail1'))
		print('is detail6', self.bd.is_detail('detail6'))
"""
test = Test()
test.test_bd()
test.test_give_all_details()
test.test_is_engine()
test.test_is_detail()
"""
