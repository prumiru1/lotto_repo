#!/usr/bin/env python

# make sure to install these packages before running:
# sudo pip3 install pandas
# sudo pip3 install sodapy

import pandas as pd
from sodapy import Socrata
import json
import time
from datetime import datetime as dt
import os


lotto_apiurl = {"powerball":"d6yy-54nr", "megamillion": "5xaw-6ayf"}

def updateLotto(lotto_name):
	try:
		f = open(lotto_name, "r")
		f_json = json.loads(f.read())
		f.close()
		# print(type(f_json), f_json["win_nums"][0]["date"])
		#print(type(f.read()))

		# Unauthenticated client only works with public data sets. Note 'None'
		# in place of application token, and no username or password:
		client = Socrata("data.ny.gov", None)

		# Example authenticated client (needed for non-public datasets):
		# client = Socrata(data.ny.gov,
		#                  MyAppToken,
		#                  userame="user@example.com",
		#                  password="AFakePassword")

		# First 2000 results, returned as JSON from API / converted to Python list of
		# dictionaries by sodapy.
		results = client.get(lotto_apiurl[lotto_name], limit=20)

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
				if (lotto_name == "megamillion"):
					numdata_new.insert(0, {"date": date_proc.strftime("%Y/%m/%d"), "nums": row['winning_numbers'] + " " + row['mega_ball']});
					# print(date_proc, row['multiplier'], row['winning_numbers'], row['mega_ball'])
				else:
					numdata_new.insert(0, {"date": date_proc.strftime("%Y/%m/%d"), "nums": row['winning_numbers']});
					# print(date_proc, row['multiplier'], row['winning_numbers'])
			else:
				break

		if (len(numdata_new) > 0):
			print(lotto_name, "| added data: ", numdata_new, "\n")

			for idx, numdata in enumerate(numdata_new):
				f_json["win_nums"].insert(0, numdata);
			f_json_str = json.dumps(f_json, indent=3)

			f = open(lotto_name, "w")
			f.write(f_json_str)
			f.close()

			if len(numdata_new) > 0:
				# os.system("bash git_lotto.sh")
				os.system('git add -A && git commit -m "' + lotto_name + ': ' + f_json["win_nums"][0]["date"] + '" && git push')
		else:
			print(lotto_name, "| No change\n")

	except Exception as e:
		print(type(e), "---", repr(e))

#-----------------------------------

while (True):
	updateLotto("powerball")
	updateLotto("megamillion")

	# time.sleep(1) 
	time.sleep(3*60*60) # 3 hour


