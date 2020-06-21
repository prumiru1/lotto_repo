#!/usr/bin/env python

# make sure to install these packages before running:
# sudo pip3 install pandas
# sudo pip3 install sodapy

import pandas as pd
from sodapy import Socrata
import json
import time
from datetime import datetime as dt

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.ny.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.ny.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")


while (True):
	try:
		f = open("powerball", "r")
		f_json = json.loads(f.read())
		f.close()
		# print(type(f_json), f_json["win_nums"][0]["date"])
		#print(type(f.read()))

		# First 2000 results, returned as JSON from API / converted to Python list of
		# dictionaries by sodapy.
		results = client.get("d6yy-54nr", limit=20)

		# Convert to pandas DataFrame
		results_df = pd.DataFrame.from_records(results)
		# print(type(results_df))

		# lotto_data = []
		# for index, row in results_df.iterrows():
		# 	date_proc = row['draw_date']			
		# 	lotto_data.append({"date": date_proc, "nums": row['winning_numbers']})
		# 	#print(row['draw_date'], row['multiplier'], row['winning_numbers'])
		# lotto_json = json.dumps({"name": "Power Ball", "win_nums": lotto_data})
		# print(lotto_json)

		numdata_new = []
		# f_json["win_nums"][0]["date"] = "2020/06/03"
		for index, row in results_df.iterrows():
			date_proc = row['draw_date']		
			f_lastest_date = dt.strptime(f_json["win_nums"][0]["date"], "%Y/%m/%d")
			date_proc = dt.strptime(date_proc[:10], "%Y-%m-%d")	

			if (f_lastest_date < date_proc):
				numdata_new.insert(0, {"date": date_proc.strftime("%Y/%m/%d"), "nums": row['winning_numbers']});
				# print(date_proc, row['multiplier'], row['winning_numbers'])
			else:
				break
		print("Added data: ", numdata_new, "\n")

		for idx, numdata in enumerate(numdata_new):
			f_json["win_nums"].insert(0, numdata);
		f_json_str = json.dumps(f_json)
		# print(f_json_str)

		f = open("powerball", "w")
		f.write(f_json_str)
		f.close()

	except Exception as e:
		print(type(e), "---", repr(e))

	time.sleep(60*60) # 1 hour