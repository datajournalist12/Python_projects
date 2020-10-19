#Program to scape stock ticker symbols off the NYSE website

from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("https://www.nyse.com/listings_directory/stock")

for item in range(645):

	string = driver.page_source

	entry = """https://www.nyse.com/quote/"""
	exit = """</a></td><td>"""
	temp1 = 0 #This var holds the number of the first bracket
	temp2 = 0 #Second bracket holder
	flag = False #Tells program whether or not to look for a right backet
	results = []

	for index in range(len(string)):
		if string[index:index+len(entry)] == entry:
			temp1 = index+len(entry)
			flag = True
		if flag == True and string[index:index+len(exit)] == exit:
			temp2 = index
			flag = False
			results.append(string[temp1:temp2])
			print(string[temp1:temp2])

	driver.find_element_by_xpath("""//*[@id="content-aa395ece-e341-4621-9695-3642148ea198"]/div/div[2]/div[2]/div/ul/li[8]/a""").click()
	time.sleep(3)


print(results)