import connect
from models import Author, Quote
from pprint import pprint


def find_quote(author):
    print(author)
    quotes = Quote.objects()
    count = 1
    for quote in quotes:
        if quote.author.fullname == author:
            print(f"Quote-{count}: {quote.quote}")
            count += 1


def find_tag(tag):
    quotes = Quote.objects()
    for quote in quotes:
        if tag in quote.tags:
            print(f'Author: {quote.author.fullname}, tag: "{tag}":\n Quote: {quote.quote}')


def find_tags(tags: list):
    quotes = Quote.objects()
    for quote in quotes:
        for tag in tags:
            if tag in quote.tags:
                print(f'Author: {quote.author.fullname}, tag: "{tag}":\n Quote: {quote.quote}')


def main(user_input):
    command = user_input.split(':')
    if len(command) >= 2:
        if command[0] == 'name':
            find_quote(author=command[1])
        elif command[0] == 'tag':
            find_tag(tag=command[1])
        elif command[0] == 'tags':
            for tag in command[1]:
                list_tags = command[1].split(',')
            find_tags(tags=list_tags)
    else:
        print(f'No "{user_input}" command')


if __name__ == '__main__':
    while True:
        user_input = input(f'Enter author or tag(s): ')
        if user_input == 'exit':
            exit()
        main(user_input)
