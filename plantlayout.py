#!/usr/bin/python3

import csv
from random import randrange

def layout(csvwriter, items):
    knuth_shuffle(items)

    for i in range(5):
        row = [""]
        for j in range(5):
            row.append(items[i*5+j])
        print(row)
        csvwriter.writerow(row)


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



items = []


with open('plantlist.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        name=row[0] + " " + row[1]
        print(name)
        items.append(name)

print(items)

with open('layouts.csv', mode="w") as layouts:
    writer = csv.writer(layouts, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for n in range(12):
        print("layout number {}".format(n))
        writer.writerow(["layout number", n])
        layout(writer,items)
        writer.writerow([])
        print()


