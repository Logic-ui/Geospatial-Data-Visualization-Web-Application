import sqlite3
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    flash,
    redirect,
    jsonify,
    send_from_directory,
)
from werkzeug.exceptions import abort
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template("post.html", post=post)


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
    return render_template("create.html")


@app.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            conn = get_db_connection()
            conn.execute(
                "UPDATE posts SET title = ?, content = ?" " WHERE id = ?",
                (title, content, id),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("edit.html", post=post)


@app.route("/<int:id>/view", methods=("GET",))
def view_post(id):
    post = get_post(id)
    if post is None:
        flash("Post not found!")
        return redirect(url_for("index"))

    return render_template("view.html", post=post)


@app.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post["title"]))
    return redirect(url_for("index"))


@app.route("/<int:id>/delete", methods=("GET", "POST"))
def delete_post_route(id):
    post = get_post(id)
    if post is None:
        flash("Post not found!")
        return redirect(url_for("index"))

    if request.method == "POST":
        delete.post(id)
        flash("Post has been deleted.")
        return redirect(url_for("index"))

    return render_template("delete.html", post=post)


def user():
    return []


# Define route for '/map'
@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/your-python-endpoint")
def get_markers():
    markers = [
        {"lat": 33.72, "lng": 73.06, "popup": "F7"},
        {"lat": 33.738818, "lng": 73.102141, "popup": "Prime minster House"},
        {"lat": 33.730722, "lng": 73.099235, "popup": "National assembly"},
        {"lat": 33.6511816, "lng": 73.07598, "popup": "Rawalpindi Cricket Stadium"},
        {"lat": 33.9056829, "lng": 73.392674, "popup": "Murree"},
        {
            "lat": 33.64999771118164,
            "lng": 73.15585327148438,
            "popup": "Comsat University Islamabad",
        },
        {"lat": 30.197838, "lng": 71.4719683, "popup": "Multan"},
        {"lat": 31.5656822, "lng": 74.3141829, "popup": "Lahore"},
        {"lat": 24.8546842, "lng": 67.0207055, "poup": "Karachi"},
        {"lat": 6.3110548, "lng": 20.5447525, "poup": "OUaka"},
        {"lat":40.741895,"lng":-73.989308,"poup":"New York"},
    ]
    return jsonify(markers)


# Route for the bar chart
@app.route("/bar-chart")
def bar_chart():
    categories = ["Category A", "Category B", "Category C"]
    values = [10, 20, 30]

    fig_bar = go.Figure([go.Bar(x=categories, y=values, name="Bar Chart")])
    bar_chart_html = pio.to_html(fig_bar, full_html=False)

    return render_template("bar_chart.html", bar_chart_html=bar_chart_html)


# Route for the stacked bar chart
@app.route("/stacked-bar-chart")
def stacked_bar_chart():
    categories = ["Category A", "Category B", "Category C"]
    values_1 = [10, 15, 20]
    values_2 = [5, 10, 15]

    fig_stacked_bar = go.Figure()
    fig_stacked_bar.add_trace(go.Bar(x=categories, y=values_1, name="Series 1"))
    fig_stacked_bar.add_trace(go.Bar(x=categories, y=values_2, name="Series 2"))
    fig_stacked_bar.update_layout(barmode="stack", title="Stacked Bar Chart")
    stacked_bar_chart_html = pio.to_html(fig_stacked_bar, full_html=False)

    return render_template(
        "stacked_bar_chart.html", stacked_bar_chart_html=stacked_bar_chart_html
    )


if __name__ == "__main__":
    app.run(debug=True)
