from bs4 import BeautifulSoup
import csv
import random, time
import requests
import urllib.request
import csv

url = []
month = []
day = []
l_weather = []
e_weather = []
temp = []

headers = ["Month","Day","Lunch","Dinner","Temp"]

def weathercode(weath):
	if weath == "晴れ":
		return 1
	if weath == "曇":
		return 2
	if weath == "雷":
		return 5
	if weath == "雨":
		return 3
	if weath == "雪":
		return 4
	return 6

for i in range(1,10):
	url.append('https://weather.goo.ne.jp/past/817/20180'+str(i*100)+"/")
	print(i,url[i-1])
for i in range(10,13):
	url.append('https://weather.goo.ne.jp/past/817/2018'+str(i*100)+"/")
	print(i,url[i-1])

#connect
for i in range(1,13):
	print(i)
	response = requests.get(url[i-1])  #check if page exists or not
	if str(response) == "<Response [200]>": #only do stuff if exists, otherwise just skip
		time.sleep(0.040)
		#parse html and save to beautiful soup object
		soup = BeautifulSoup(response.text, "html.parser")

		for d in range(1,32):
			#print(str('class=\"day\">'+str(d)))
			#print(str(soup))
			if (str(d)+"</td>") in str(soup):
				#print(str(soup).split((str(d)+"</td>"))[1].split("</tr>")[0])
				offset = 7-int((str(soup).split((">"+str(d)+"</td>"))[1].split("</tr>")[0]).count("day"))
				#print(d,offset)

				lunch_weather = str(soup).split(">"+str(d)+"</td>")[1].split("天気")[0].split("12時")[1].split("<td>")[offset].split("alt=\"")[1].split("\"")[0]
				dinner_weather = str(soup).split(">"+str(d)+"</td>")[1].split("天気")[0].split("15時")[1].split("<td>")[offset].split("alt=\"")[1].split("\"")[0]
				temps = str(soup).split(">"+str(d)+"</td>")[1].split("天気")[0].split("最高気温")[1].split("<td>")[offset].split("red\">")[1].split("<")[0]

				month.append(i)
				day.append(d)
				l_weather.append(weathercode(lunch_weather))
				e_weather.append(weathercode(dinner_weather))
				temp.append(temps)

	time.sleep(2)

with open("weather.csv", "w", newline='', encoding="utf-16") as myfile: #, encoding="utf-8"
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)  #	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	wr.writerow(headers)
	for yy in range(0,len(month)):
		row_items=[month[yy],day[yy],l_weather[yy],e_weather[yy],temp[yy]]
		wr.writerow(row_items)