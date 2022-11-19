from flask import Flask, request
import json
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
      host="mysql",
      user="root",
      passwd="root",
      database="campaign"
)

@app.route("/voucher", methods=['POST'])
def get_voucher():
    try:
        data = request.get_json()
        print(data)
        segment_name = data["segment_name"]

        print(f"Fetching voucher for segment_name: {segment_name}")

        total_orders = data["total_orders"]
        cursor = mydb.cursor()
        sql = "select voucher_amount from voucher_log where total_orders >=14 AND total_orders <= 37 order by count desc limit 1";
        cursor.execute(sql)

        result = {}
        for row in cursor.fetchall():
            result["voucher_amount"] = row[0]

        return result

    except BaseException as e:
        return (f"Exception: {e}")

    
if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0', debug=True)
