from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return cls(id, name)

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors')
        authors = [cls(id=row[0], name=row[1]) for row in cursor.fetchall()]
        conn.close()
        return authors

    @classmethod
    def get_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], name=row[1]) if row else None

    def update(self, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE authors SET name = ? WHERE id = ?', (name, self.id))
        conn.commit()
        conn.close()
        self.name = name

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM authors WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()