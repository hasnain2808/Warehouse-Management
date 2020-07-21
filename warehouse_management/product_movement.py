from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
import sqlite3

from warehouse_management.db import get_db

bp = Blueprint("product_movement", __name__, url_prefix="/product_movement")


@bp.route("/add_product_movement", methods=("GET", "POST"))
def add_product_movement():
    """Add a new product Movement
    """
    if request.method == "POST":
        quantity = request.form["quantity"]
        from_location_id = request.form["from_location_id"]
        to_location_id = request.form["to_location_id"]
        product_id = request.form["product_id"]
        error = None
        if not quantity:
            error = "quantity is required."
        elif not from_location_id:
            error = "from_location_id is required."

        elif to_location_id == "0" and from_location_id == "0":
            error = "to_location_id or from_location_id is required."
        elif to_location_id == "0":
            to_location_id = None
        elif from_location_id == "0":
            from_location_id = None
        elif not product_id:
            error = "product_id is required."
        if error is None:

            try:
                db = get_db()
                db.execute(
                    "INSERT INTO ProductMovement (from_location, to_location, product_id, qty) VALUES (?,?,?, ?)",
                    (from_location_id, to_location_id, product_id, quantity),
                )
                db.commit()
                return redirect(url_for("product_movement.add_product_movement"))
            except sqlite3.Error as error:
                print(error)
                return render_template("error_occured.html")

        flash(error)
    try:
        db = get_db()
        location_list = db.execute("SELECT location_id FROM Location",)
        product_list = db.execute("SELECT product_id FROM Product ",)
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")
    locations = [location[0] for location in location_list]
    return render_template(
        "product_movement/add_product_movement.html",
        res={"locations": locations, "product_list": product_list,},
    )


@bp.route("/view_product_movement", methods=["GET"])
def view_product_movement():
    """Returns all movements recorded

    """
    try:
        db = get_db()
        prod_mov = db.execute(
            "SELECT  movement_id, timestamp, from_location, to_location, product_id, qty FROM ProductMovement Order By (timestamp)"
        )
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")

    return render_template(
        "product_movement/view_product_movement.html", result=prod_mov
    )


@bp.route("/delete_product_movement/<id>", methods=["GET"])
def delete_product_movement(id):
    """Delete a row in product movement marked by id

    Args:
        id (string): id of the row to be deleted

    """
    try:
        db = get_db()
        print(id)
        db.execute("DELETE FROM ProductMovement  WHERE movement_id = (?)", (id,))
        db.commit()
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")
    return redirect(url_for("product_movement.view_product_movement"))


@bp.route("/update_product_movement/<id>", methods=["GET", "POST"])
def update_product_movement(id):
    """Update the movements

    Args:
        id (string): [id of the row to be updated]

    """
    if request.method == "POST":
        quantity = request.form["quantity"]
        from_location_id = request.form["from_location_id"]
        to_location_id = request.form["to_location_id"]
        product_id = request.form["product_id"]
        error = None
        if not quantity:
            error = "quantity is required."
        elif not from_location_id:
            error = "from_location_id is required."

        elif to_location_id == "0" and from_location_id == "0":
            error = "to_location_id or from_location_id is required."
        elif to_location_id == "0":
            to_location_id = None
        elif from_location_id == "0":
            from_location_id = None
        elif not product_id:
            error = "product_id is required."
        if error is None:
            try:
                db = get_db()
                db.execute(
                    "UPDATE  ProductMovement SET from_location = ?, to_location = ?, product_id = ?, qty = ? WHERE movement_id = ?",
                    (from_location_id, to_location_id, product_id, quantity, id),
                )
                db.commit()
                return redirect(url_for("product_movement.view_product_movement"))
            except sqlite3.Error as error:
                print(error)
                return render_template("error_occured.html")
        flash(error)

    try:
        db = get_db()
        prod_mov = db.execute(
            "SELECT   movement_id ,from_location, to_location, product_id, qty FROM ProductMovement  where movement_id = (?) Order By (timestamp)",
            (id,),
        ).fetchone()
        location_list = db.execute("SELECT location_id FROM Location ",)
        product_list = db.execute("SELECT product_id FROM Product ",)
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")

    locations = [location[0] for location in location_list]

    return render_template(
        "product_movement/update.html",
        res={
            "prod_mov": prod_mov,
            "locations": locations,
            "product_list": product_list,
        },
    )


@bp.route("/get_report", methods=("GET", "POST"))
def get_report():
    """Generate Report as the total number of items at each warehouse
    """

    try:
        # Select All rows in the product movement
        db = get_db()
        prod_mov = db.execute(
            "SELECT  from_location, to_location, product_id, qty FROM ProductMovement Order By (timestamp)",
        )
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")
    location = {}
    # iterate over all rows returned
    for movement in prod_mov:
        # get the current row values in local variables
        curr_product = movement[2]
        curr_from_location = movement[0]
        curr_to_location = movement[1]
        qty = movement[3]
        # Update the relevant values in the grid and store as dictionary
        # Although negative quantity movements is not very useful but handling it just in case it is given by the user
        if curr_from_location:
            if curr_from_location in location:
                if curr_product in location[curr_from_location]:
                    location[curr_from_location][curr_product] -= qty
                else:
                    location[curr_from_location][curr_product] = -1 * (qty)
            else:
                temp = {}
                temp[curr_product] = -1 * (qty)
                location[curr_from_location] = temp

        if curr_to_location:
            if curr_to_location in location:
                if curr_product in location[curr_to_location]:
                    location[curr_to_location][curr_product] += qty
                else:
                    location[curr_to_location][curr_product] = qty
            else:
                temp = {}
                temp[curr_product] = qty
                location[curr_to_location] = temp
    return render_template("product_movement/view_report.html", result=location)
