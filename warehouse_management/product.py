from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from warehouse_management.db import get_db

bp = Blueprint("product", __name__, url_prefix="/product")

import sqlite3


@bp.route("/add_product", methods=("GET", "POST"))
def add_product():
    """Add a new product

    """
    if request.method == "POST":
        try:
            product_id = request.form["product_id"]
            print(product_id)
            db = get_db()
            db.execute("INSERT INTO Product (product_name) VALUES (?)",
                (product_id,)
            )
            db.commit()
            return render_template("product/add_product.html",res={"visible":True}) 
        except sqlite3.Error as error:
            print(error)
            return render_template("error_occured.html")
     
    return render_template("product/add_product.html",
                    res={"visible":False},
    )


@bp.route("/view_product", methods=["GET"])
def view_product():
    """Returns details of all products

    """
    try:
        db = get_db()
        products = db.execute("SELECT product_id, product_name FROM Product")
        return render_template("product/view_product.html", result=products)
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")


@bp.route("/delete_product/<id>", methods=["GET"])
def delete_product(id):
    """Delete a product Marked by id

    Args:
        id (String): id of the product to be deleted
    """
    try:
        db = get_db()
        db.execute("DELETE FROM Product  WHERE product_id = (?)", (id,))
        db.commit()
        return redirect(url_for("product.view_product"))
    except sqlite3.Error as error:
        print(error)
        return render_template("error_occured.html")
