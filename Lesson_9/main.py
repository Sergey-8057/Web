import connect
import json

from models import Author, Quote
from parsing import parsing, url


def create_bd_authors():
    list_authors_for_quotes = list()
    with open('authors.json', 'r') as fd:
        list_authors = json.load(fd)
    for iter_author in list_authors:
        author = Author(
        fullname = iter_author['fullname'],
        born_date = iter_author['born_date'],
        born_location = iter_author['born_location'],
        description = iter_author['description']
        )
        list_authors_for_quotes.append(author)
        author.save()
    print('Database "author" created.')
    return list_authors_for_quotes


def create_bd_quotes(list_authors):
    with open('quotes.json', 'r') as fd:
        list_quotes = json.load(fd)
    for iter_quote in list_quotes:
        fullname_author = iter_quote['author']
        author = next((a for a in list_authors if a.fullname == fullname_author), None)
        if author:
            quote = Quote(
            tags = iter_quote['tags'],
            author = author,
            quote = iter_quote['quote']
            )
        quote.save()
    print('Database "quote" created.')


if __name__ == '__main__':
    parsing(url)
    list_authors = create_bd_authors()
    create_bd_quotes(list_authors)
    print('Completed!')
