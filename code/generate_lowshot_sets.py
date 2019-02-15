#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os  
import csv
import random as rnd

from argparse import ArgumentParser

""" ompc_generate_lowshot_sets.py
Generates low shot sets from the full train set
"""

SIZES = [.01,.02,.05,.075,.1,.2,.5,.75,1.]
ITERATIONS = 10

full_dataset = []

def stratifyed_shuffled_subset(data, size):
	""" returns a stratifyed, but shuffled subset of lenght *size* """
	dataset_dict = {}
	subset = []

	rnd.shuffle(data)

	for entry in data:
		label = entry[0]
		text = entry[1]
		if label not in dataset_dict:  # if the label is not yet in the dict
		   dataset_dict[label] = []
		f = dataset_dict[label]
		f.append(text)

	for key in dataset_dict:
		key_set = dataset_dict[key]
		for entry in key_set[: int(len(key_set) * size)]:
			subset.append([key, entry])

	rnd.shuffle(subset)
	return subset

def write_dataset(data, size, iteration):
	with open("lowshot/lowshot_" + str(size) +"_" + str(iteration) + ".csv", "w") as file_write:
		writer = csv.writer(file_write, delimiter=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
		for entry in data:
			writer.writerow(entry)

def write_dataset_fasttext(data, size, iteration):
	with open("lowshot/lowshot_" + str(size) +"_" + str(iteration) + ".csv", "w") as file_write:
		writer = csv.writer(file_write, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
		for entry in data:
			label = "__label__" + entry[0]
			writer.writerow([label, entry[1]])


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('-fastText', action='store_true')
	args = parser.parse_args()

	print("writing files in fastText format:", args.fastText)

	createFolder('./lowshot/')	

	with open("train.csv") as full_file:
		reader = csv.reader(full_file, delimiter=';', quotechar='\'')
		for row in reader:
			full_dataset.append(row)

	# sets a seed for reproducability
	rnd.seed(42)

	size_counter = 0
	for size in SIZES:
		for iteration in range(ITERATIONS):
			print("Generating iteration %.0f of size %.3f" % (iteration, size))
			subset = stratifyed_shuffled_subset(full_dataset, size)

			if not args.fastText:
				write_dataset(subset, str(size_counter) + "_" + str(size), iteration)
			if args.fastText:
				write_dataset_fasttext(subset, str(size_counter) + "_" + str(size), iteration)
			
		size_counter+=1
