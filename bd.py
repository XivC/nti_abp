"""
	Вся работа с БД будет тут
"""


class BD:
	def __init__(self, cursor, name_bd):
		""" инитиализация курсора и бд"""
		self.cursor = cursor
		self.__str__ = name_bd

	def create_bd(self):
		""" Creating new base of date"""
		print('TEST creating BD')
		return True
