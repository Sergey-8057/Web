wrong_word = input("You: ")
right_words = ['phone', 'change', 'add', 'show', 'exit', 'good bye']


rw_dict = {}
for right_word in right_words:
    sum_lit = 0
    for lit_rw in right_word:
        for lit_ww in wrong_word:
            if lit_ww == lit_rw:
                sum_lit += 1

    rw_dict.update({sum_lit: right_word})
    # print(sum_lit, ':', right_word)

# print(rw_dict)
fig_rw_dict = []
for key in rw_dict.keys():
    fig_rw_dict.append(key)
# print(fig_rw_dict)
max_fig = max(fig_rw_dict)
# print(max(fig_rw_dict))
for key, value in rw_dict.items():
    if key == max_fig:
        close_to_right_word = rw_dict.get(key)
        # print(close_to_right_word)


def w_r():
    for right_word in right_words:
        if wrong_word == right_word:
            return right_word
    else:
        return f"Your command {wrong_word} is not correct! Did you mean {close_to_right_word}?"


print(w_r())
