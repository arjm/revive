#!/usr/bin/env python

"""test.py: Check test cases for revive"""

__author__      = "Arjit Malviya"

import json, requests, unittest

URL = "http://api:9999/voucher"

class TestReview(unittest.TestCase):

	def test_frequent_segment_valid_input(self):
		data = {"customer_id": 123, "country_code": "Peru", "last_order_ts": "2018-05-03 00:00:00", "first_order_ts": "2017-05-03 00:00:00", "total_orders": 15, "segment_name": "frequent_segment"}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post(URL, data=json.dumps(data), headers=headers)
		self.assertEqual(r.text.strip(), "{\n  \"voucher_amount\": 2640.0\n}")


	def test_frequent_segment_invalid_input(self):
		data = {"customer_id": 123, "country_code": "Peru", "last_order_ts": "2018-05-03 00:00:00", "first_order_ts": "2017-05-03 00:00:00", "total_orders": -20, "segment_name": "frequent_segment"}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post(URL, data=json.dumps(data), headers=headers)
		self.assertEqual(r.text.strip(), "{\n  \"voucher_amount\": 0\n}")


	def test_recency_segment_valid_input(self):
		data = {"customer_id": 123, "country_code": "Peru", "last_order_ts": "2018-05-03 00:00:00", "first_order_ts": "2017-05-03 00:00:00", "total_orders": 15, "segment_name": "recency_segment"}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post(URL, data=json.dumps(data), headers=headers)
		self.assertEqual(r.text.strip(), "{\n  \"voucher_amount\": 2640.0\n}")


	def test_recency_segment_invalid_input(self):
		data = {"customer_id": 123, "country_code": "Peru", "last_order_ts": "2027-05-03 00:00:00", "first_order_ts": "2018-05-03 00:00:00", "total_orders": 15, "segment_name": "recency_segment"}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post(URL, data=json.dumps(data), headers=headers)
		self.assertEqual(r.text.strip(), "{\n  \"voucher_amount\": 0\n}")

if __name__ == '__main__':
    unittest.main()

