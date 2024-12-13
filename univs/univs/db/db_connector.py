import sqlite3

class DB_CLIENT:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_con(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
    
    def execute_select_query(self, query):
        return self.cursor.execute(query)
    
    def execute_insert_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def execute_many_inserts(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()

    # Create necessary tables for the scrapers
    def init_db(self):
        self.cursor.execute("CREATE TABLE rankings(university_name, pos, ranker)")
        self.cursor.execute("CREATE TABLE programs(university_name, university_alias, program_name)")
        self.cursor.execute("CREATE TABLE addresses(university_name, university_alias, city, state, country, zipcode)")

    def drop_db(self):
        self.cursor.execute("DROP TABLE rankings")
        self.cursor.execute("DROP TABLE programs")
        self.cursor.execute("DROP TABLE addresses")