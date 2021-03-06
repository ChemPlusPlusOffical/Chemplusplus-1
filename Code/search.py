'''
This is the file which will search the chemistry stack exchange
in order to give answers in the application
'''

from tkinter import *

import requests

from bs4 import BeautifulSoup

import re

import threading




def search(t):
	query = t.split(" ")
	formatted_query = ""
	for i in range(len(query)):
		formatted_query += query[i]
		formatted_query += "+"
	formatted_query = formatted_query[:len(formatted_query)-1]

	to_search = f'https://chemistry.stackexchange.com/search?q={formatted_query}'

	init_site = requests.get(to_search).text

	soup = BeautifulSoup(init_site, 'html.parser')

	page_1_results = soup.find_all(class_="question-hyperlink")[:3]



	for i in range(len(page_1_results)):
		page_1_results[i] = str(page_1_results[i]).split("href=\"")[1]
		page_1_results[i] = page_1_results[i].split("\"")[0]


	searches = []

	to_return  = []

	for i in range(len(page_1_results)):
		searches.append(f"https://chemistry.stackexchange.com{page_1_results[i]}")

	for i in searches:
		site = requests.get(i)

		soup2 = BeautifulSoup(site.text, "html.parser")

		results = soup2.find_all(class_='s-prose js-post-body')

		total = ''

		for e in range(len(results)):
			total += results[e].text

		total += f"\n\n\n\nSource:\t{i}"

		to_return.append(total)

	return to_return

def search_gui(res):
	search_window = Tk()

	search_window.geometry("1200x500")

	search_window.title("Search Results")

	search_window.resizable(False, False)

	search_window.configure(bg = '#373e40')

	scroll = Scrollbar(search_window)

	scroll.pack(side = RIGHT, fill = Y)

	results_title = Label(search_window, text = f'Results for : {_Search_Entry.get()}', font = ("Montserrat", 24), bg = "#373e40", fg = "#ffffff")

	results_title.pack()

	#35 characters 




	texts = []

	result = Text(search_window, width = 120, height = 25, wrap = WORD, font = ("Montserrat", 10), yscrollcommand = scroll.set)
	result.insert(END, res[0])
	result.place(x = 50, y = 50 )

	scroll.config(command = result.yview)

	global INDEX
	INDEX = 0

	_Forward = Button(search_window, text = ">", font = ("Montserrat", 10), bg = "#373e40", fg = "#ffffff", command = lambda:switch(res, result, INDEX+1))

	_Backward = Button(search_window, text = "<", font = ("Montserrat", 10), bg = "#373e40", fg = "#ffffff", command = lambda:switch(res, result, INDEX-1))

	_Forward.place(x = 40, y = 0)

	_Backward.place(x = 0, y = 0)


def switch(res, txt, index):
	global INDEX

	if index > len(res)-1 or index < 0:
		return None

	if index == INDEX + 1:
		INDEX += 1
	elif index == INDEX - 1:
		INDEX -= 1


	txt.delete('1.0', END)
	txt.insert(END, res[index])

	
def create_search(t):
	global _Search_Frame, _Search_Entry, _Search_Enter

	_Search_Frame = LabelFrame(t, text = 'Search', width = 400, height = 80, font = ("Montserrat", 10), bg = "#373e40", fg = "#ffffff")

	_Search_Frame.place(x = 790, y = 10)

	_Search_Entry = Entry(_Search_Frame, bg = '#ffffff', fg = '#121212', font = ("Montserrat", 10), width = 42)

	_Search_Entry.insert(0, "Search")

	_Search_Entry.place(x = 7, y = 0)

	_Search_Enter = Button(_Search_Frame, text = "Enter Search", command = lambda:search_gui(search(_Search_Entry.get())),
		font = ("Montserrat", 10), width = 40)

	_Search_Enter.place(x = 5, y = 25)


