import json
import requests
from bs4 import BeautifulSoup


url = 'https://quotes.toscrape.com/'


def parsing_author(path_author):
	author_response = requests.get(path_author)
	author_soup = BeautifulSoup(author_response.text, 'lxml')
	fullname_author = author_soup.find('h3').get_text()
	born_date_author = author_soup.find('span', class_='author-born-date').get_text()
	born_born_location = author_soup.find('span', class_='author-born-location').get_text()
	description_author = author_soup.find('div', class_='author-description').get_text()
	data_author = {
		'fullname': fullname_author.strip(),
		'born_date': born_date_author.strip(),
		'born_location': born_born_location.strip(),
		'description': description_author.strip()
		}
	return data_author, fullname_author


def parsing_quote(quote, fullname_author):
	tags = quote.select("div.tags a")
	list_tag = [a.text for a in tags]
	author = fullname_author
	quote_author = quote.find('span', class_='text').get_text()
	data_quote = {
		'tags': list_tag,
		'author': author.strip(),
		'quote': quote_author.strip()
		}
	return data_quote


def save_authors(list_authors):
	with open("authors.json", "w", encoding="utf-8") as fd:
		json.dump(list_authors, fd, ensure_ascii=False, indent=2)
	print('Data "Authors" saved to file "author.json"')


def save_quotes(list_quotes):
	with open("quotes.json", "w", encoding="utf-8") as fd:
		json.dump(list_quotes, fd, ensure_ascii=False, indent=2)
	print('Data "Quotes" saved to file "quotes.json"')


def parsing(url):
	page = 1
	list_authors = list()
	list_quotes = list()
	while True:
		page_site = f'page/{page}/'
		page_url = url + page_site
		response = requests.get(page_url)
		soup = BeautifulSoup(response.text, 'lxml')
		next_page_link = soup.find('li', class_='next')
		quotes = soup.find_all('div', class_='quote')
		for quote in quotes:
			link_author = quote.find('a')["href"]
			path_author = url + link_author [1:]
			data_author = parsing_author(path_author)
			if data_author[0] not in list_authors:
				list_authors.append(data_author[0])
				print(f'Author "{data_author[0]["fullname"]}" added to the list.')
			data_quote = parsing_quote(quote=quote, fullname_author=data_author[1])
			list_quotes.append(data_quote)
		page += 1
		if response.status_code != 200 or next_page_link == None:
			save_authors(list_authors)
			save_quotes(list_quotes)
			break
		