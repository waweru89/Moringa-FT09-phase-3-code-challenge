from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return cls(id, name, category)

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines')
        magazines = [cls(id=row[0], name=row[1], category=row[2]) for row in cursor.fetchall()]
        conn.close()
        return magazines

    @classmethod
    def get_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], category=row[2]) if row else None

    def update(self, name=None, category=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (name, self.id))
            self.name = name
        if category:
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (category, self.id))
            self.category = category
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM magazines WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()