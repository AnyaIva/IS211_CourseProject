import os
from builtins import str
from typing import List

import sqlite3 as sql

from flask import Flask, request, session, render_template, url_for

# import Flask, session, render_template, request, redirect, url_for

import helpers
import model
# from flask_session import Session

books: List[model.Book] = []
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

db = sql.connect('books.db')
print("Opened database successfully")
db.close()

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if session.get("username") is None:
            return render_template("login.html")
    else:
        try:
            if request.method == "POST":
                name = request.form.get("user_name")
                pwd = request.form.get("user_pwd")
                with sql.connect("books.db") as con:
                    cur = con.cursor()
                    stmnt = cur.execute("SELECT * FROM users WHERE user_name = :name AND user_pwd = :password",
                                        {"name": name, "password": pwd}).fetchone()
                    if stmnt is None:
                        return render_template("login.html", error_message="Wrong username or password")
                    else:
                        # cur.execute("INSERT INTO users (user_name, user_pwd) VALUES (:name, :pwd)", {
                        #     "name": name, "pwd": pwd})
                        con.commit()
                        session["user_name"] = name
                        return render_template("welcome.html", message="Login successful")
        except Exception as ex:
            print(ex)
            con.rollback()
            return render_template("login.html", error_message="Error on the server")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        # Try to register user
        try:
            name = request.form.get("user_name")
            pwd = request.form.get("user_pwd")

            with sql.connect("books.db") as con:
                cur = con.cursor()
                stmnt = cur.execute("SELECT * FROM users WHERE user_name = :name", {"name": name})
                found = stmnt.fetchone()
                if found is None:
                    cur.execute("INSERT INTO users (user_name, user_pwd) VALUES (:name, :pwd)", {
                        "name": name, "pwd": pwd})
                    con.commit()
                    session["user_name"] = name
                    return render_template("welcome.html", message="Registration successful")
                else:
                    return render_template("register.html", error_message="Username already exists")

        except Exception as ex:
            print(ex)
            con.rollback()
            return render_template("register.html", error_message="Error on the server")


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        # result_check = is_provided("search")
        return render_template("welcome.html")
    elif request.method == "POST":
        searchkey = request.form.get("text")
        results = helpers.lookup(searchkey)
        books = results
        return render_template("welcome.html", results=results, input_value=searchkey)


@app.route("/logout")
def logout():
    session["user_name"] = None
    # return redirect(url_for("index"))


@app.route('/viewcatalogue', methods=["GET", "POST"])
def viewcatalogue():
    if request.method == "GET":
        isbn = request.args.get("book")
        mybook = helpers.getBook(isbn)
        return render_template("viewcatalogue.html", book=mybook)
    elif request.method == "POST":
        return render_template("")


@app.route("/addbook", methods=["GET", "POST"])
def addbook():
    if request.method == "GET":
        isbn = request.args.get("book")
        try:
            mybook = helpers.getBook(isbn)
            print(books)
            print(mybook)

            title = mybook.volumeInfo.title
            author = mybook.volumeInfo.authors
            if mybook.volumeInfo.authors is None:
                author = "None"
            year = mybook.volumeInfo.publishedDate
            if mybook.volumeInfo.publishedDate is None:
                year = "None"
            book_id = mybook.id
            user_name = session["user_name"]
            with sql.connect("books.db") as con:
                cur = con.cursor()
                stmnt = cur.execute("SELECT * FROM bookview WHERE book_id = :book_id and user_name = :user_name",
                                    {"book_id": book_id, "user_name": user_name})
                found = stmnt.fetchone()
                if found is None:
                    cur.execute(
                        "INSERT INTO bookview (book_title, book_author, publication_year, book_id, user_name) VALUES "
                        "(:title, :author, :year, :book_id, :user_name)",
                        {
                            "title": title, "author": author, "year": year, "book_id": book_id, "user_name": user_name})
                    con.commit()
                    helpers.fetchmybooks(user_name)

                    return render_template("viewbooks.html", message="Added successful",
                                           results=helpers.fetchmybooks(user_name))
                else:
                    return render_template("viewbooks.html", message="Book Already exist",
                                           results=helpers.fetchmybooks(user_name))

        except Exception as ex:
            print(ex.__str__())
            return render_template("viewbooks.html", message="Added successful")
            # con.rollback()


@app.route('/viewbooks', methods=["GET", "POST"])
def viewbooks():
    try:
        user_name = session["user_name"]
        results = helpers.fetchmybooks(user_name)
        print(results)
        return render_template("viewbooks.html", results=results)
    except Exception as ex:
        print("Hello")
        print(ex.__str__())
        return render_template("welcome.html", message="Could Not retrieve List")


@app.route('/delete', methods=["GET", "POST"])
def deletebook():
    try:
        isbn = request.args.get("book")
        user_name = session["user_name"]
        helpers.deleteBook(user_name, isbn)
        results = helpers.fetchmybooks(user_name)
        return render_template("viewbooks.html", results=results, message="Book Deleted successfully")
    except Exception as ex:
        print(ex.__str__())
        return render_template("viewbooks.html", message="Could Not Delete Book")


if __name__ == "__main__":
    app.run(debug=True)
