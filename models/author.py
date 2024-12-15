import sqlite3
from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine

class Author:
    def __init__(self, id=None, name=None):
        if id is None:  # This means a new author needs to be created
            self.create(name)
        else:
            self.id = id
            self.name = name

    def create(self, name):
        if not name:
            raise ValueError("Author name must be provided.")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        self.id = cursor.lastrowid  # Get the id of the newly created author
        self.name = name
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer.")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):  # Prevent changing the name after initialization
            raise AttributeError("Author name cannot be changed once set.")
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    def articles(self):
        """
        Returns a list of articles associated with this author.
        Uses SQL JOIN to fetch articles related to this author.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles WHERE author_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    def magazines(self):
        """
        Returns a list of magazines associated with this author.
        Uses SQL JOIN to fetch distinct magazines related to this author.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row[0], row[1], row[2]) for row in rows]

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"
