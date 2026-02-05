from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import json
import os

app = Flask(__name__)
CORS(app)

db = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route("/place-order", methods=["POST"])
def place_order():
    data = request.json

    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO orders 
        (customer_name, email, address, books, total_amount)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data["name"],
            data["email"],
            data["address"],
            json.dumps(data["cart"]),
            data["total"]
        )
    )
    db.commit()

    return jsonify({"message": "Order placed successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
