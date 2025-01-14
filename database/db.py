'''
	Set up a database with sqlite3 
'''
import sqlite3

class Database:
	def __init__(self, db_path:str):
		self.db_path = db_path
		self.connection = sqlite3.connect(self.db_path)
		self.cursor = self.connection.cursor()
	
	def execute(self, query:str, values:tuple = ()):
		self.cursor.execute(query, values)
		self.connection.commit()
	
	def selectall(self, query:str, values:tuple = ()):
		self.cursor.execute(query, values)
		return self.cursor.fetchall()
	
	def selectone(self, query:str, values:tuple = ()):
		self.cursor.execute(query, values)
		return self.cursor.fetchone()
	
	def close(self):
		self.connection.close()

