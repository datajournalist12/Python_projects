#Scrapes Facebook friends list

def spider():

	import os
	import time
	from selenium import webdriver
	from bs4 import BeautifulSoup

	sleep_tracker = 0

	#Gets the website I want

	chrome_path = r"/Library/Frameworks/Python.framework/Versions/3.6/bin/chromedriver"
	driver = webdriver.Chrome(chrome_path)
	driver.get("https://www.facebook.com")
	
	iterations = 200
	prefix = input("Enter prefix: ")
	company = input("Enter company: ")
	
	for item in range(iterations):
		username_string = input("Enter username: ")

		user = ''
		if "/" in username_string:
			for position in range(len(username_string)):
				if "/" == username_string[position]:
					position_mark = position
					

					company = username_string[position_mark + 1:]
					user = username_string[:position_mark]

		if "/" in username_string:
			username_string = user


		driver.get("https://www.facebook.com/" + username_string + "/friends")
		time.sleep(5)

		#Checks for closed friends list

		tagger = ''

		source_code = driver.page_source
		soup = BeautifulSoup(source_code, "html.parser")

		a_tags = soup.find_all("a")
		divs = soup.find_all("div")

		for a_tag in a_tags:
			if "eng_tid" in str(a_tag):
				tagger = str(a_tag)

		for div in divs:
			if "Want Followers of Your Own?" in str(div):
				tagger = ''

		if tagger:

			#Scrolls webpage to end

			source_code = driver.page_source
			tracker = False

			while tracker == False:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

				source_code = driver.page_source
				soup = BeautifulSoup(source_code, "html.parser")
				h3_tags = soup.find_all("h3")
				time.sleep(0.7)

				for h3_tag in h3_tags:
					if "More About" in str(h3_tag):
						print(h3_tag)
						tracker = True

			#Parses out element (script and a tags) we are interested in
			#Then searches parsed element to determine if appropriate for ext. eng.

			code_aTag = []
			code_script = []

			code_source_name = []
			code_source_nickname = []
			code_source = []
			workplace = []

			soup = BeautifulSoup(source_code, "html.parser")

			a_tags = soup.find_all("a")

			for a_tag in a_tags:
				if "eng_tid" in str(a_tag):
					code_aTag.append(str(a_tag))

			scripts = soup.find_all("script")

			for source_name in scripts:
				if "schema.org" in str(source_name):
					code_source_name.append(str(source_name))
					
			for source in scripts:
				if "entity_id" in str(source):
					code_source.append(str(source))

			noscripts = soup.find_all("noscript")

			for source_nickname in noscripts:
				if "friends" in str(source_nickname):
					code_source_nickname.append(str(source_nickname))

			spans = soup.find_all("span")
				
			for span in spans:
				if '''</a> at <a class="_39g5"''' in str(span):
					workplace.append(str(span))



			#Extraction engine pulls data from element

			cleaned_list = []
			close_keys = []

			def extraction_engine(opener, closer):

				if "profile.php?id=" in cleaned_code and "?fref" in closer:
					print("No nickname")
					cleaned_list.append("No nickname")

				else:
				
					for position in range(len(cleaned_code)):
						if opener == cleaned_code[position:position + len(opener)]:
							open_key = position + len(opener)

					for position in range(len(cleaned_code)):
						if closer == cleaned_code[position:position + len(closer)]:
							close_key = position

					#print(cleaned_code[open_key:close_key])
					cleaned_list.append(cleaned_code[open_key:close_key])


			for cleaned_code in code_aTag:
				extraction_engine("user.php?id=", "&amp;extragetparams")
				extraction_engine("""">""", "</a>")
				extraction_engine("""href="https://www.facebook.com/""", "?fref")
				
				for cleaned_code in code_source:
					extraction_engine('''"entity_id":"''', '''"}],''')
				for cleaned_code in code_source_name:
					if "jobTitle" in cleaned_code:
						extraction_engine('''"Person","name":"''', '''","jobTitle''')
					elif "PostalAddress" in cleaned_code:
						extraction_engine('''"Person","name":"''', '''","address"''')
					else:
						extraction_engine('''"Person","name":"''', '''","affiliation"''')
				for cleaned_code in code_source_nickname:
					extraction_engine("URL=/", "/friends")

			#Converts list to GDF format, and saves file

			tracker = 0
			filename = prefix + cleaned_list[4] + ".gdf"
			secondary_list = ''
			tertiary_list = []


			print("nodedef>name VARCHAR,label VARCHAR,nickname VARCHAR,company VARCHAR, scraped VARCHAR")
			with open(os.path.join('/Users/alexheeb/Documents/gdfs',filename), 'w') as part:
						part.write("nodedef>name VARCHAR,label VARCHAR,nickname VARCHAR,company VARCHAR, scraped VARCHAR" + "\n")

			print(cleaned_list[3] + ''',"''' + cleaned_list[4] + '''",''' + cleaned_list[5] + "," + company)

			with open(os.path.join('/Users/alexheeb/Documents/gdfs',filename), 'a', encoding='utf-8') as part:
				part.write(cleaned_list[3] + ''',"''' + cleaned_list[4] + '''",''' + cleaned_list[5] + "," + company + "," + "Scraped" + "\n")

			for item in cleaned_list:
				if tracker == 0:
					secondary_list += item
				if tracker == 1:
					secondary_list += ''',"''' + item + '''",'''
				if tracker == 2:
					secondary_list += item
					secondary_list += ",,"
					tertiary_list.append(secondary_list)
				tracker = tracker + 1
				if tracker == 6:
					tracker = 0
					secondary_list = ''

			for element in tertiary_list:
				print(element)

			with open(os.path.join('/Users/alexheeb/Documents/gdfs',filename), 'a', encoding='utf-8') as part:
						for element in tertiary_list:
							part.write(element + "\n")

			print("edgedef>node1 VARCHAR,node2 VARCHAR")
			with open(os.path.join('/Users/alexheeb/Documents/gdfs',filename), 'a', encoding='utf-8') as part:
				part.write("edgedef>node1 VARCHAR,node2 VARCHAR" + "\n")

			lowerbody_string = ''
			lowerbody_list = []
			tracker = 0

			for item in cleaned_list:
				if tracker == 0:
					lowerbody_string += item + ","
				if tracker == 3:
					lowerbody_string += item
					lowerbody_list.append(lowerbody_string)
				tracker = tracker + 1
				if tracker == 6:
					tracker = 0
					lowerbody_string = ''

			for item in lowerbody_list:
				print(item)

			with open(os.path.join('/Users/alexheeb/Documents/gdfs',filename), 'a', encoding='utf-8') as part:
				for element in lowerbody_list:
					part.write(element + "\n")

			#special section workplace

			cleaned_list = []
			workplace_list = []
			tracker = 0

			for cleaned_code in workplace:
				extraction_engine("https://www.facebook.com/", '''">''')
				extraction_engine('''">''', "</a></span>")

			#Lazy patch for / problem
			for item in cleaned_list:
				workplace_list.append(item)

			pi_string = ''
			for line in cleaned_list:
				if tracker ==  0:
					pi_string += '"' + line.rstrip() + '",'
					tracker = 1

				elif tracker ==  1:
					pi_string += '"' + line.rstrip() + '"'
					tracker = 0
					print(pi_string)
					with open("workplaces.csv", 'a', encoding='utf-8') as element:
						element.write(pi_string + "\n")
					pi_string = ''

			#Pauses program to avoid detection
			sleep_times = [1,1,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15,1,4,1,1,6,9,4,1,6,1,15]

			time.sleep(60 * sleep_times[sleep_tracker])
			sleep_tracker = sleep_tracker + 1
		else:
			print("Closed friends list")
