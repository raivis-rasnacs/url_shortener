from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash
)
import sqlite3
from uuid import uuid4

con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()

app = Flask(__name__)
app.config["FLASK_ENV"] = "development"
app.config["SECRET_KEY"] = "secret!"

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/shorten_url", methods = ["POST"])
def shorten_url():
    if request.method == "POST":
        url = request.form.get("url")

        unique_id = str(uuid4())[:5]
        shortened_url = f"127.0.0.1:5000/{unique_id}"

        sql = """INSERT INTO Entries
        (entry_id, url, shortened_url)
        VALUES (?, ?, ?);"""

        cur.execute(sql, (
            str(uuid4()),
            url,
            shortened_url
        ))
        con.commit()
        flash("Saīsinātais url saglabāts!")
        return render_template("url_view.html", url=shortened_url)

@app.route("/<shortened_url>")
def open_url(shortened_url):
    print(shortened_url)
    sql = """SELECT url FROM Entries
    WHERE shortened_url = ?;"""
    res = cur.execute(sql, (
        f"127.0.0.1:5000/{shortened_url}", 
    ))
    url = res.fetchall()
    if url:
        url = url[0][0]
        return redirect(f"{url}")
    else:
        print(1)
        flash("Šāds url neeksistē!")
        return redirect("/")

if __name__ == "__main__":
    if app.config["FLASK_ENV"] == "development":
        app.run(debug=True)
