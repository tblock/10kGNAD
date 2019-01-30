#!/usr/bin/env python
# coding: utf-8

import csv
import collections

from sklearn.model_selection import train_test_split

""" split_articles_into_train_test.py:

processes the dataset and splits the dataset into a training- and testset
"""

SPLIT_PERCENTAGE = .1


def write_datasets(data, name):
    """ write a csv file in a normal and optinally in the fastText format """

    with open(name + ".csv", "w") as file_write:
        writer = csv.writer(file_write, delimiter=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)
	
# Optionally wirte in the fastText format
#	with open("fsttxt_" + name + ".csv", "w") as file_write:
#      writer = csv.writer(file_write, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
#       for row in data:
#           label = row[0]
#           label = "__label__" +  label
#           writer.writerow([label, row[1]])


if __name__ == "__main__":

    labels = []
    texts = []

    # read full dataset file
    with open("articles.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='\'')
        for row in reader:
            labels.append(row[0])
            texts.append(row[1])

    # split dataset
    trn_texts, tst_texts, trn_labels, tst_labels = train_test_split(texts, labels, test_size=SPLIT_PERCENTAGE, random_state=42, stratify=labels)

    # write train and test datasets
    train = []
    test = []
    
    for i in range(len(trn_labels)):
        train.append([trn_labels[i], trn_texts[i]])
    
    for i in range(len(tst_labels)):
        test.append([tst_labels[i], tst_texts[i]])

    write_datasets(train, "train")
    write_datasets(test, "test")


