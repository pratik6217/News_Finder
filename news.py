import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# with open('key.key', 'w') as file:
	# file.write(key.decode())
with open('key.key', 'r') as file:
	key = file.read().encode()

f = Fernet(key)

# with open('api_key.key', 'w') as file:
	# file.write(f.encrypt('79f277fc4923480faa856e19ee212317'.encode()).decode())

with open('api_key.key', 'r') as file:
	apiKey = f.decrypt(file.read().encode()).decode()

q = ''
date = ''
sortBy = 'popularity'
# apiKey = ''


option = st.sidebar.selectbox("Menu", ['Home','Everything', 'Top Headlines'])
if option == 'Home':
	st.title('Welcome to Newsify')
	st.subheader('Find the best in class news articles here just with a single click of a button.')
	st.write()
elif option == 'Everything':
	q = st.text_input('Enter the Keyword for finding the news:')
	st.write()
	date = st.date_input('Enter the date from which you want to search the most popular news:')
	submit = st.button('submit')

	if (q == '' or date == '') and submit:
		st.warning('The Keyword cannot be Null !!')
	elif (q and date) and submit:
		url = 'https://newsapi.org/v2/everything?q={q}&from={date}&sortBy={sB}&apiKey={apiKey}'.format(q= q, date= str(date), sB= sortBy, apiKey= apiKey)
		response = requests.get(url).json()
		status = response['status']
		number_of_articles = response['totalResults']
		if response:
			if status == 'ok':
				try:
					st.write("Total number of articles found = ", number_of_articles)
					for value in response['articles']:
						st.subheader("Title: {title}".format(title= value['title']))
						st.write('Description: {description}'.format(description= value['description']))
						st.text('Name: {name}'.format(name= value['source']['name']))
						st.text('Author: {author}'.format(author= value['author']))
						st.write('Referance URL: {url}'.format(url= value['url']))
						st.write()
				except Exception as e:
					st.error(e)
			else:
				st.error(response['status'])
		else:
			st.error("Nothing Found")

elif option == "Top Headlines":
	st.title("Top Headlines:")
	st.write()

	url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=79f277fc4923480faa856e19ee212317'
	response = requests.get(url).json()
	status = response['status']
	number_of_articles = response['totalResults']
	if response:
		if status == 'ok':
			try:
				st.write("Total number of articles found = ", number_of_articles)
				for value in response['articles']:
					st.subheader("Title: {title}".format(title= value['title']))
					st.write('Description: {description}'.format(description= value['description']))
					st.text('Name: {name}'.format(name= value['source']['name']))
					st.text('Author: {author}'.format(author= value['author']))
					st.write('Referance URL: {url}'.format(url= value['url']))
					st.write()
			except Exception as e:
					st.error(e)
		else:
			st.error(response['status'])
	else:
		st.error("Nothing Found")
