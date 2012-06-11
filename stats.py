# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

import urllib2

## dictionaries used to store statistics
# keys: renaming rules, values: occurrences count
rules = dict()
durations = {
            '0': 0, # Minutes only (e.g.: 100m)
            '1': 0 # Hours and minutes (e.g.: 1h40m)
            }
languages = {
            '0': 0, # English name (e.g.: English)
            '1': 0 # 3-letters (e.g.: ENG)
            }
separators = {
            '0': 0, # , (comma-space)
            '1': 0, # - (space-dash-space)
            '2': 0 #  (space)
            }

# compose url
url = "http://almoviesrenamer.appspot.com/stats"
# get data from web service
f = urllib2.urlopen(url)
# read statistics, split into lines and remove last (empty) line
stats = f.read().split('\n')[:-1]

# for each line
for stat in stats:
    # split rules using "&"
    stat = stat.split('&')
    # current renaming rule is not into dictionary
    if not stat[0] in rules:
        # add it with count 1
        rules.update({stat[0]: 1})
    else:
        # increase count
        rules[stat[0]] += 1
    # increase count for duration from current statistic
    durations[stat[1]] += 1
    # increase count for language from current statistic
    languages[stat[2]] += 1
    # increase count for separator from current statistic
    separators[stat[3]] += 1
# sort rules based on occurrences count
rules = sorted(rules.items(), key = lambda x: x[1], reverse = True)

# print rules statistics
print("\n" + "-"*10 + "rules" + "-"*10)
for rule in rules:
    print(rule[0] + ": " + str(rule[1]))
# print durations statistics
print("\n" + "-"*10 + "durations" + "-"*10)
print("Minutes only (e.g.: 100m): " + str(durations['0']))
print("Hours and minutes (e.g.: 1h40m): " + str(durations['1']))
# print languages statistics
print("\n" + "-"*10 + "languages" + "-"*10)
print("English name (e.g.: English): " + str(languages['0']))
print("3-letters (e.g.: ENG): " + str(languages['1']))
# print separators statistics
print("\n" + "-"*10 + "separators" + "-"*10)
print(", (comma-space): " + str(separators['0']))
print("- (space-dash-space): " + str(separators['1']))
print(" (space): " + str(separators['2']))









