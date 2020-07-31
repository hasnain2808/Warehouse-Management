from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from warehouse_management.db import get_db

import sqlite3

bp = Blueprint("location", __name__, url_prefix="/location")


@bp.route("/add_location", methods=("GET", "POST"))
def add_location():
    """Add a new Location
    """
    if request.method == "POST":
        try:
            db = get_db()
            db.execute("INSERT INTO Location DEFAULT VALUES",)
            db.commit()
            return render_template("location/add_location.html",res={"visible":True},)
        except sqlite3.Error as error:
            print(error)
            return render_template("error_occured.html")
    return render_template("location/add_location.html",res={"visible":False},)


@bp.route("/view_location", methods=["GET"])
def view_location():
    """Returns all location
    """
    try:
        db = get_db()
        locations = db.execute("SELECT location_id FROM Location")
        return render_template("location/view_location.html", result=locations)
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")


@bp.route("/delete_location/<id>", methods=["GET"])
def delete_location(id):
    """Deletes a location marked by id

    Args:
        id (String): Id of the location to be deleted
    """
    try:
        db = get_db()
        db.execute("DELETE FROM Location  WHERE location_id = (?)", (id,))
        db.commit()
        return redirect(url_for("location.view_location"))
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")
