from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Create an author using the Author model
    new_author = Author.create(author_name)

    # Create a magazine using the Magazine model
    new_magazine = Magazine.create(magazine_name, magazine_category)

    # Create an article using the Article model
    new_article = Article.create(article_title, article_content, new_author.id, new_magazine.id)

    # Query the database for all records (this is now handled by the model methods)
    all_authors = Author.get_all()
    all_magazines = Magazine.get_all()
    all_articles = Article.get_all()

    # Display results
    print("\nMagazines:")
    for magazine in all_magazines:
        print(magazine)

    print("\nAuthors:")
    for author in all_authors:
        print(author)

    print("\nArticles:")
    for article in all_articles:
        print(article)

if __name__ == "__main__":
    main()