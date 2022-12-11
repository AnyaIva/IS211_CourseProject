import csv


from sqlalchemy import create_engine, null
from sqlalchemy.orm import scoped_session, sessionmaker

create_engine = null
try:
    # Set up database
    engine = create_engine('sqlite:///C:\\sqlitedbs\\books.db', echo=True)
    db = scoped_session(sessionmaker(bind=engine))
except Exception:
    raise Exception("Could not connect to database")


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book {title}, {author}, {year} with ISBN = {isbn}")
    db.commit()


# if __name__ == "__main__":
#     main()
