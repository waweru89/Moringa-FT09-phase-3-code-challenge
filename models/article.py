import sqlite3
from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of the Author class.")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        
        self.title = title
        self.author_id = author.id
        self.magazine_id = magazine.id
        
        # Create the new article entry in the database
        self.create(title)

    def create(self, title):
        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be between 5 and 50 characters.")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, author_id, magazine_id)
            VALUES (?, ?, ?)
        ''', (title, self.author_id, self.magazine_id))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) < 5 or len(value) > 50:
            raise ValueError("Title must be between 5 and 50 characters.")
        self._title = value

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM authors WHERE id = ?
        ''', (self.author_id,))
        row = cursor.fetchone()
        conn.close()
        return Author(row[0], row[1]) if row else None

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM magazines WHERE id = ?
        ''', (self.magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return Magazine(row[0], row[1], row[2]) if row else None

    def __repr__(self):
        return f'<Article {self.title}>'

