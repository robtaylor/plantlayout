#!/usr/bin/python3

import csv
import pprint
from random import randrange

pp = pprint.PrettyPrinter(indent=4)


def layout(csvwriter, items):
    knuth_shuffle(items)

    odd_row = True
    odd_column = True
    index = 0
    for i in range(7):
        row = [""]
        for j in range(7):
            if i==3 and j==3:
                row.append("")
            elif odd_row and odd_column:
                row.append(items[index])
                index = index + 1 
            elif not odd_row and odd_column:
               	row.append(items[index])
                index = index + 1 
            else:
                row.append("")
            odd_column = not odd_column
        csvwriter.writerow(row)
        odd_row = not odd_row


def knuth_shuffle(items):
    """
    Fisher-Yates shuffle or Knuth shuffle which name is more famous.
    See <http://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle> for detail
    Type : [a] -> None (shuffle inplace)
    Post constrain: Should be list
    Post constrain: return array of the same length of input
    """

    for i in range(len(items)):
        j = randrange(i, len(items))
        items[i], items[j] = items[j], items[i]


def load_plantlist(filename):
    items = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # skip headings
        next(csv_reader)

        for row in csv_reader:
            items.append(row[0])
    return items


def load_bag_list(filename):
    items = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            items.append({'number': int(row[0]), 'depth': row[1]})
    return items


def output_one_layout(csvfile, bag, plants):
    writer = csv.writer(layouts, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    title = "bag"
    bag_data = ['number', 'depth', 'set', 'water']
    for k in bag_data:
        title += f' {k}: {bag[k]}'
    writer.writerow([title])
    layout(writer, plants)
    writer.writerow([])


def list_experiments():
    exps = []
    for n in range(12):
        set = 1 if n < 6 else 2
        water = True if (n % 6 < 3) else False
        exps.append({'set': set, 'water': water})
    return exps


# list of bags as on ground, and depth
bags = load_bag_list('bags.csv')
print("Bag list:")
pp.pprint(bags)

# Create a list of all the different experiment combinations for 200 depth
experiments_200 = list_experiments()
experiments_400 = list_experiments()

print('200 depth experiments:')
pp.pprint(experiments_200)
print('400 depth experiments:')
pp.pprint(experiments_400)

# randomise them
knuth_shuffle(experiments_200)
knuth_shuffle(experiments_400)

# assign expeiments to bags

for bag in bags:
    if bag['depth'] == '200':
        bag.update(experiments_200.pop())
    if bag['depth'] == '400':
        bag.update(experiments_400.pop())

# save as csv
csv_columns = ['number', 'depth', 'set', 'water']
with open('experiments.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in bags:
        writer.writerow(data)

# Load our plant lists for the two sets
set_1_plants = load_plantlist('plantlist1.csv')
set_2_plants = load_plantlist('plantlist2.csv')


# Output layouts for each bag
with open('layouts.csv', mode="w+") as layouts:
    for bag in bags:
        plants = set_1_plants if bag['set'] == 1 else set_2_plants
        output_one_layout(layouts, bag, plants)
