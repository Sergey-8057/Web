from fuzzywuzzy import process

def fuzzy_match(user_input, options):
    highest = process.extractOne(user_input, options)
    return f'With probability "{highest[1]}%" you tried to type the "{highest[0]}" command. Try again more accurate!'