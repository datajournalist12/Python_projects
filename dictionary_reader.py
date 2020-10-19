#Program to take an excel file, convert into Pandas dataframe, and convert into JSON data.

import pandas as pd
x = pd.read_excel("file:///Users/alexheeb/Documents/turtle_races.xlsx")

data = {}
for date in x['Projected 2021 Date/Time']:
	try:
		data[str(date.month) + "/" + str(date.day)] = {}
	except:
		pass



for index in range(len(x['Projected 2021 Date/Time'])):
	try:
		data[str(x['Projected 2021 Date/Time'][index].month) + "/" + str(x['Projected 2021 Date/Time'][index].day)].update({x['State'][index]:0})
	except:
		pass



for index in range(len(x['Projected 2021 Date/Time'])):
	try:
		data[str(x['Projected 2021 Date/Time'][index].month) + "/" + str(x['Projected 2021 Date/Time'][index].day)][x['State'][index]] += 1
	except:
		pass


#for item in data:
#	temp = data[item]
#	print(item, temp.get('Kansas',0) + temp.get('Oklahoma',0))




