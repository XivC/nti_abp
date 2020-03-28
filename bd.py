import sqlite3
from datetime import datetime


def give_day():
	today = datetime.today()
	return (str(today.year)+"-"+str(today.month)+"-"+str(today.day))


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
			CREATE TABLE IF NOT EXISTS receipts
			(name, seria, count, name_admin, id_receipt, date)
		""")

		self.conn.commit()

		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS requests 
			(id INTEGER PRIMARY KEY AUTOINCREMENT, create_date TEXT, change_date TEXT, delete_date TEXT, buyer TEXT 
			, status TEXT) 
		""")
		self.conn.commit()

		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS fsb
			(buyer TEXT, bool INTEGER)
		""")
		self.conn.commit()

		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS buy_drons
			(id, dron_name, count)
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
		self.cursor.execute('SELECT type FROM details WHERE name_detail = ?', (name_engine,))
		data = self.cursor.fetchone()[0]
		return data == 'Аккумуляторные батареи' or data == 'batter'

	def give_all_details(self):
		"""Возвращает список всех деталий"""
		self.cursor.execute('SELECT* FROM "main"."details"')
		return self.cursor.fetchall()

	def write_receipt_in_bd(self, data):
		"""
		Записывают в базу данных поставки
		[(name, seria, count, name_admin, id_receipt, date), ]
		:param data: список кортежей в каждом кортеже строчка из бд
		:return: True
		"""

		self.cursor.executemany("""INSERT INTO receipts values (?, ?, ?, ?, ?, ?)""", data)
		self.conn.commit()
		return True

	def give_all_less_date(self, date):
		"""
		:param date:  string type 2020-02-26
		:return: all collums with dates
		"""
		self.cursor.execute("SELECT * FROM receipts WHERE date <= ?", (date,))
		return self.cursor.fetchall()

	def give_list_of_last_details(self, date):
		data = self.give_all_less_date(date)
		ms = dict()
		for collum in data:
			if not (collum[0], collum[4]) in ms:
				ms[(collum[0], collum[4])] = 0
			ms[(collum[0], collum[4])] += collum[2]
		ls = []
		for key in ms:
			ls.append((key[0], key[1], ms[key]))
		return ls

	def give_drons(self):
		self.cursor.execute("""
			SELECT * FROM drons
		""")
		return self.cursor.fetchall()

	def create_new_request(self, create_date, buyer, list_of_drons, status='Создано', change_date='', delete_date=""):
		"""
		list_of_drons = [(dron_name, count), ...]
		:return:
		"""
		self.cursor.execute(
			"""INSERT INTO requests (create_date, change_date,
		  delete_date, buyer, status ) values (?, ?, ?, ?, ?)""", (create_date, change_date,
		  delete_date, buyer, status)
		)
		self.conn.commit()

		self.cursor.execute("""
		SELECT last_insert_rowid()  FROM requests
		""")
		id = self.cursor.fetchone()[0]

		for dron in list_of_drons:
			self.cursor.execute("""
				INSERT INTO buy_drons VALUES (?, ?, ?)
			""", (id, dron[0], dron[1]))
			self.conn.commit()

		#TODO test me
		if not self.check_buyer_in_fsb(buyer):
			self.add_buyer_in_fsb(buyer)
			self.change_status_request(request_id=id, status="Запрошено разрешение у ФСБ")
		elif self.give_status_buyer_fsb(buyer):
			self.change_status_request(request_id=id, status='Произвести сборку')
		else:
			self.change_status_request(request_id=id, status='Анулирована', delete_date=give_day())

	def give_all_requests(self):
		"""
		:return ms = [[id, create_date, change_date, status, sum], ...]
		"""
		self.cursor.execute(
			"""
				SELECT id, create_date, change_date, status FROM requests
			"""
		)
		data = self.cursor.fetchall()
		ms = []
		for i in data:
			ms.append(i + (self.give_request_sum(i[0]),))
		return ms

	def give_request_sum(self, request_id):
		"""
		Считает сумму заказа и возвращает ее
		:param request_id: unique id of request in table
		:return: sum of request
		"""
		self.cursor.execute("""
			SELECT dron_name, count FROM buy_drons WHERE id = ?
		""", (request_id,))
		data = self.cursor.fetchall()
		sum = 0
		for dron in data:
			sum += self.give_dron_sum(dron)
		return sum

	def give_dron_sum(self, dron):
		self.cursor.execute("""
			SELECT cost FROM drons WHERE name_dron = ?
		""", (dron[0],))
		cost = self.cursor.fetchone()[0]
		return cost * dron[1]

	def change_status_request(self, request_id, status, delete_day=''):
		"""
		Меняет статус заказа

		Создана
		Идет сборка
		Готова к отгрузке
		Запрошено разрешение у ФСБ
		Анулирована
		Отгружена

		:param request_id: unique id in table of requests
		:return: True, if accessly, and False another
		"""
		if status == "Готова к отгрузке" :
			data = self.check_count_of_details(request_id)
			if data:
				self.minus_details(data)
			else:
				return False

		self.cursor.execute("""
			UPDATE requests SET status = (?), change_date = (?), delete_date = (?) WHERE id = (?)
		""", (status, give_day(), delete_day, request_id))
		self.conn.commit()
		return True


	def check_count_of_details(self, request_id):
		self.cursor.execute("""
			SELECT * FROM buy_drons""")# WHERE id = (?)""", (request_id,))
		drons = self.cursor.fetchall()
		need = {}
		for dron in drons:
			self.cursor.execute("""
				SELECT * FROM dron_map WHERE name = (?)
			""", (dron[1],))
			details = self.cursor.fetchall()
			for detail in details:
				if not detail[2] in need:
					need[detail[2]] = 0
				need[detail[2]] = int(detail[3]) * int(dron[2])
		for key in need:
			sm = 0
			self.cursor.execute("""
				SELECT count FROM receipts  WHERE name = ?
			""", (key, ))
			details = self.cursor.fetchall()
			for detail in details:
				sm = sm + int(detail[0])
				if need[key] - sm > 0:
					return False
		return need


	def minus_detail(self, data):
		print(data)
		ms = []
		for key in data:
			tp = (key, '', -data[key], 'Bulat', -1, give_day())
			ms.append(tp)
		print(ms)
		self.write_receipt_in_bd(ms)
		return True


	def add_buyer_in_fsb(self, buyer, status=0):
		self.cursor.execute("""
			INSERT INTO fsb values (?, ?)
		""", (buyer, status))
		self.conn.commit()
		# TODO TESTING THAT FUNCTION

	def check_buyer_in_fsb(self, buyer):
		self.cursor.execute("""
			SELECT count(*) FROM fsb WHERE buyer=(?)
		""", (buyer,))
		return self.cursor.fetchone()[0] == 1

	def change_status_fsb(self, buyer, status=1):
		"""
		Меняет статус у фсб

		0 - если нет разрешения
		1 - если да

		:param buyer: Имя покупателя строки
		:return: True/False if okey
		"""
		self.cursor.execute("""
			UPDATE fsb SET status = (?) WHERE buyer=(?)
		""", (status, buyer))
		self.conn.commit()
		# TODO test me please, oh god, please deeper
		return True


class Filter:

	def __init__(self):
		import datetime
		self.datetime = datetime

	def is_digit(self, string):
		if not str(string).isdigit():
			return (True, "строка {} не записана в {} базу данных, так как содержится буква в числе")
		return (False, "Все хорошо")

	def check_date(self, date='2020-12-01'):
		date_format = '%Y-%m-%d'
		try:
			date_obj = self.datetime.datetime.strptime(date, date_format)
			return True
		except ValueError:
			return False

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
			flag1, string1 = self.is_digit(dron[0])
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


class Test1:

	def __init__(self):
		self.bd = BD("Test1BD.sqlite")
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

	def test_requests(self):
		self.bd.create_new_request(
			create_date='2019-12-03',
			delete_date='',
			change_date='2019-12-03',
			buyer='Zaripov',
			status='Создано',
			list_of_drons=[('dron1', 3)]
		)
		# self.bd.change_status_request()
		print(self.bd.give_all_requests())

	def test(self):
		#self.test_requests()
		self.bd.give_all_requests()
		self.bd.change_status_request(11, 'all okey')
		print(self.bd.give_request_sum(11))
		return True

Test1().test()

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

	def test_receipts_add(self):
		print('--TESTING RECEIPTS')
		id = '00002'
		date = '2020-10-1'
		name = 'Zaripov'
		data = [
			['АКБ Сириус 1', 'AJLKF22', 1, name, id, date],
			['АКБ Сириус 1', 'AJLKF23', 1, name, id, date],
			['Лопасть РР2', '', 23, name, id, date]
		]
		self.bd.write_receipt_in_bd(data)

	def test_is_digit(self):
		print('--TESTING IS DIGIT')
		print(self.bd.filter.is_digit(12))
		print(self.bd.filter.is_digit(15))
		print(self.bd.filter.is_digit("ter"))

	def test_filters(self):
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
		print('--TESTING FILTERS')
		data = self.bd.filter.filter_details_table(details_table)
		print(data)
		data = self.bd.filter.filter_dron_map(dron_map)
		print(data)
		data = self.bd.filter.filter_drons_table(drons_table)
		print(data)

	def test_give_all_colums_less_date(self, date='2020-12-31'):
		data = self.bd.give_all_less_date(date)
		print(data)

	def test_give_me_spisok_of_receipts(self, date='2020-12-31'):
		data = self.bd.give_list_of_last_details(date)
		return data


"""
test = Test()
test.test_bd()
test.test_give_all_details()
test.test_is_engine()
test.test_is_detail()
test.test_receipts_add()
"""
"""
test = Test()
test.test_is_digit()
test.test_filters()
"""
"""
test = Test()
test.test_give_all_colums_less_date('2021-12-03')
print(test.test_give_me_spisok_of_receipts())
"""

db = BD()
db.create_tables()
data = db.check_count_of_details(1)
if data:
	db.minus_detail(data=data)
else:
	print('NO')
