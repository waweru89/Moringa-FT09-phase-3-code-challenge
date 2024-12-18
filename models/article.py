from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       (title, content, author_id, magazine_id))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return cls(id, title, content, author_id, magazine_id)

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles')
        articles = [cls(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) for row in cursor.fetchall()]
        conn.close()
        return articles

    @classmethod
    def get_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) if row else None

    def update(self, title=None, content=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        if title:
            cursor.execute('UPDATE articles SET title = ? WHERE id = ?', (title, self.id))
            self.title = title
        if content:
            cursor.execute('UPDATE articles SET content = ? WHERE id = ?', (content, self.id))
            self.content = content
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articles WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()