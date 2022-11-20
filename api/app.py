from datetime import datetime
from dateutil import parser
from flask import abort, Flask, request
import json, sys
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
      host="mysql",
      user="root",
      passwd="root",
      database="campaign"
)

range_frequency = {0 : 4, 5 : 13, 12 : 37, 38 : sys.maxsize}
range_recency = {30 : 60, 61 : 90, 91 : 120, 121 : 180, 181: sys.maxsize}

@app.route("/voucher", methods=['POST'])
def get_voucher():
    try:
        data = request.get_json()
        segment_name = data["segment_name"]

        if not segment_name:
            abort(400)

        if segment_name == "frequent_segment":
            return _get_voucher_from_frequency_segement(data)
        elif segment_name == "recency_segment":
            return _get_voucher_from_recency_segement(data)

    except BaseException as e:
        return (f"Exception: {e}")


@app.errorhandler(400)
def internal_error(error):
    return "400: Bad input", 400


def _get_voucher_from_frequency_segement(data):
    """Gets the voucher amount from the frequency segement"""
    total_orders = data["total_orders"]
    range = _get_frequency_range(total_orders)

    result = {}

    if range:
        cursor = mydb.cursor()
        sql = f"select voucher_amount from voucher_frequent_segment where total_orders >={range[0]} AND total_orders <= {range[1]} order by count desc limit 1";
        print(sql)
        cursor.execute(sql)        
        for row in cursor.fetchall():
            result["voucher_amount"] = row[0]
    else:
        result["voucher_amount"] = 0
    return result


def _get_frequency_range(total_orders: int):
    """Gets the min and max range for the frequency segement"""
    for key, value in range_frequency.items():
        if total_orders >= key and total_orders <= value:
            return (key, value)


def _get_voucher_from_recency_segement(data):
    """Gets the voucher amount from the recency segement"""
    last_order_date_str = data["last_order_ts"]

    try:
        last_order_date = parser.parse(last_order_date_str)
    except BaseException as e:
        abort(400)

    last_order_delta_days = (datetime.today() - last_order_date).days
    range = _get_recency_range(last_order_delta_days)

    result = {}

    if range:
        cursor = mydb.cursor()
        sql = f"select voucher_amount from voucher_recency_segment where days_since >={range[0]} AND days_since <= {range[1]} order by count desc limit 1";
        print(sql)
        cursor.execute(sql)        
        for row in cursor.fetchall():
            result["voucher_amount"] = row[0]
    else:
        result["voucher_amount"] = 0
    return result


def _get_recency_range(last_order_delta_days: int):
    """Gets the min and max range for the frequency segement"""
    for key, value in range_recency.items():
        if last_order_delta_days >= key and last_order_delta_days <= value:
            return (key, value)

    
if __name__ == "__main__":
    app.run(port=9999, host='0.0.0.0', threaded=True)
