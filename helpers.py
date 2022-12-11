from typing import List

import requests
import json
import sqlite3 as sql

import model

books: List[model.Book] = []


def fetchmybooks(username):
    try:
        con = sql.connect("books.db")
        cur = con.cursor()
        results = []
        for row in cur.execute("SELECT * FROM bookview;"):
            if str(row[5]).strip().casefold() == str(username).strip().casefold():
                b = {"id": row[4], "title": row[1], "publishedDate": row[3], "author": row[2]}
                results.append(b)
        con.close()
        return results
    except Exception as ex:
        return []


def getBook(id):
    for b in books:
        if b.id.casefold() == id.casefold():
            return b
    return None


def lookup(search):
    """Look up search for books."""
    # Contact API
    books.clear()
    try:
        url = f'https://www.googleapis.com/books/v1/volumes?q={search}'
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        print("in req err")
        return None
    # Parse response

    search = response.json()
    print(type(search["items"]))

    for item in search["items"]:
        json_object = json.dumps(item, indent=4)
        jsonstring = json.loads(json_object)
        books.append(model.Book.from_dict(jsonstring))

    print(books[1].__str__())
    return books


def deleteBook(user_name, isbn):
    try:
        con = sql.connect("books.db")
        cur = con.cursor()
        myid = None
        for row in cur.execute("SELECT * FROM bookview;"):
            if str(row[5]).strip().casefold() == str(user_name).strip().casefold() and str(
                    row[4]).strip().casefold() == str(isbn).strip().casefold():
                myid = row[0]
                print(row)
                break

        if myid is None:
            return False

        cur = con.cursor()
        cur.execute("DELETE FROM bookview WHERE id = :myid;", {"myid": myid})
        con.commit()
        print("deleted")
        return True
    except Exception as ex:
        print(ex)
        return False
