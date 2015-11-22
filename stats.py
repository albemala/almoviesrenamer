# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

import requests

## dictionaries used to store statistics
# keys: renaming rules, values: occurrences count
rules_dict = dict()
info_dict = dict()
durations = {
    '0': 0,  # Minutes only (e.g.: 100m)
    '1': 0  # Hours and minutes (e.g.: 1h40m)
}
languages = {
    '0': 0,  # English name (e.g.: English)
    '1': 0  # 3-letters (e.g.: ENG)
}
separators = {
    '0': 0,  # , (comma-space)
    '1': 0,  # - (space-dash-space)
    '2': 0  # (space)
}

# compose url
url = "http://almoviesrenamer.appspot.com/stats"
# get data from web service
response = requests.get(url)
data = response.content.decode(encoding="UTF-8")
# read statistics, split into lines and remove last (empty) line
stats = data.split('\n')[:-1]

# for each line
for stat in stats:
    # split rules using "&"
    stat = stat.split('&')
    # current renaming rule is not into dictionary
    rule = stat[0]
    if rule not in rules_dict:
        # add it with count 1
        rules_dict.update({rule: 1})
    else:
        # increase count
        rules_dict[rule] += 1
    info = rule.split(".")
    for i in info:
        if i not in info_dict:
            # add it with count 1
            info_dict.update({i: 1})
        else:
            # increase count
            info_dict[i] += 1
    # increase count for duration from current statistic
    try:
        durations[stat[1]] += 1
    except:
        pass
    # increase count for language from current statistic
    try:
        languages[stat[2]] += 1
    except:
        pass
    # increase count for separator from current statistic
    try:
        separators[stat[3]] += 1
    except:
        pass
# sort rules based on occurrences count
rules_dict = sorted(rules_dict.items(), key=lambda x: x[1], reverse=True)

dashes = 15
# print rules statistics
print("\n" + "-" * dashes + " rules " + "-" * dashes)
for rule in rules_dict:
    print(rule[0] + ": " + str(rule[1]))
# print info statistics
print(info_dict)
print("\n" + "-" * dashes + " info " + "-" * dashes)
for info in info_dict:
    print(info + ": " + str(info_dict[info]))
# print durations statistics
print("\n" + "-" * dashes + " durations " + "-" * dashes)
print("Minutes only (e.g.: 100m): " + str(durations['0']))
print("Hours and minutes (e.g.: 1h40m): " + str(durations['1']))
# print languages statistics
print("\n" + "-" * dashes + " languages " + "-" * dashes)
print("English name (e.g.: English): " + str(languages['0']))
print("3-letters (e.g.: ENG): " + str(languages['1']))
# print separators statistics
print("\n" + "-" * dashes + " separators " + "-" * dashes)
print(", (comma-space): " + str(separators['0']))
print("- (space-dash-space): " + str(separators['1']))
print(" (space): " + str(separators['2']))
