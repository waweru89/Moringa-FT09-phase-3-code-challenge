import sqlite3
from database.connection import get_db_connection
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id is None:  # If no id is passed, create a new magazine
            self.create(name, category)
        else:
            self.id = id
            self.name = name
            self.category = category

    def create(self, name, category):
        if not name or not category:
            raise ValueError("Magazine name and category must be provided.")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
        self.id = cursor.lastrowid  # Get the id of the newly created magazine
        self.name = name
        self.category = category
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
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) == 0:
            raise ValueError("Category must not be empty.")
        self._category = value

    def articles(self):
        """
        Returns a list of articles associated with this magazine.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    def contributors(self):
        """
        Returns a list of authors associated with this magazine.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row[0], row[1]) for row in rows]

    def article_titles(self):
        """
        Returns a list of titles of all articles for this magazine.
        Returns None if no articles exist.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows] if rows else None

    def contributing_authors(self):
        """
        Returns a list of authors who have written more than 2 articles for this magazine.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row[0], row[1]) for row in rows] if rows else None

    def __repr__(self):
        return f"<Magazine(id={self.id}, name={self.name}, category={self.category})>"
