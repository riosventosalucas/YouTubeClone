#!/usr/local/bin/env python

import json
import random
from random import randrange
from datetime import timedelta
from datetime import datetime

db = open('initial-data.json', 'r')

json_data = json.loads(db.read())

db.close()

new_data = []

for data in json_data:

	start_date = datetime(2020, 1, 1)
	end_date = datetime(2021, 1, 1)

	time_between_dates = end_date - start_date
	days_between_dates = time_between_dates.days
	random_number_of_days = random.randrange(days_between_dates)

	random_date = start_date + datetime.timedelta(days=random_number_of_days)

	new_data.append(
		{
	      "model":data['model'],
	      "pk":data['pk'],
	      "fields":{
	         "title":data['fields']['title'],
	         "views":data['fields']['views'],
	         "author":data['fields']['author'],
	         "youtube_id":data['fields']['youtube_id'],
	         "thumbnail_url":data['fields']['thumbnail_url'],
	         "slug":data['fields']['slug'],
	         "active":data['fields']['active'],
	         "creation_date":str(random_date),
	         "likes":[],
	         "dislikes":[]
	      }
	   }
	)


db = open('initial-data.json', 'w')

db.write(json.dumps(new_data))


