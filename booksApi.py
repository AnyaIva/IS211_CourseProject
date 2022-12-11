import os


def getBooks():
    books = []
    for root, dirs, files in os.walk('books'):
        for name in files:
            books.append(os.path.join(root, name))
    return []
