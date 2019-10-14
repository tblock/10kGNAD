#!/usr/bin/env python
# coding: utf-8

"""
extract_dataset_from_sqlite.py.py

This exports the articles from the _One Million Posts Corpus_ and generates a 
CSV file containing a label and the text for each article.
"""

import re
import sys
import csv
import sqlite3

from tqdm import tqdm
from bs4 import BeautifulSoup
from argparse import ArgumentParser


ARTICLE_QUERY = "SELECT Path, Body FROM Articles WHERE PATH LIKE 'Newsroom/%' AND PATH NOT LIKE 'Newsroom/User%' ORDER BY Path"


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(dest="sqlite_file", action="store", help="sqlite input filename", metavar="<SQLite Database>")
    parser.add_argument(dest="csv_file", action="store", help="csv output filebame", metavar="<CSV Filename>")
    args = parser.parse_args()

    
    conn = sqlite3.connect(args.sqlite_file)
    cursor = conn.cursor()

    with open(args.csv_file, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';',quotechar='\'', quoting=csv.QUOTE_MINIMAL)

        for row in tqdm(cursor.execute(ARTICLE_QUERY).fetchall(), unit_scale=True):
            path = row[0]
            body = row[1]
            text = ""
            description = ""

            soup = BeautifulSoup(body, 'html.parser')

            # get description from subheadline 
            description_obj = soup.find('h2',{'itemprop':'description'})
            if description_obj is not None:
                description = description_obj.text
                description = description.replace("\n"," ").replace("\t"," ").strip() + ". "

            # get text from paragraphs
            text_container = soup.find('div',{'class':'copytext'})
            if text_container is not None:
                for p in text_container.findAll('p'):
                    text += p.text.replace("\n"," ").replace("\t"," ").replace("\"","").replace("'","") + " "
            text = text.strip()
            
            # remove article autors
            for author in re.findall(r"\.\ \(.+,.+2[0-9]+\)", text[-50:]): # some articles have a year of 21015..
                text = text.replace(author, ".")

            # get category from path
            category = path.split("/")[1]
            sample = [category, description + text]

            # filter empty samples, then write to csv
            if sample[1] != "":
                writer.writerow(sample)

    conn.close()
   
