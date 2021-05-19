from __future__ import print_function

import requests
import matplotlib.pyplot as plt
import json
# Barcode Detect
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

import sys
def search_book(search):
    # search books by google api
    # if isinstance(search, int):
    if search.isnumeric():
        search_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'.format(search)
    else:
        search_url = "https://www.googleapis.com/books/v1/volumes?q={}".format(search.replace(' ','+'))
    r = requests.get(url = search_url)

    print(r)


    # retrieve books metadata
    results = json.loads(r.text)
    if results['totalItems'] == 0:
        print("Could not find such books!!")
        return None

    books_list = []
    for item in results['items']:
        if 'volumeInfo' not in item:
            print(item)
            continue
        item_info = item['volumeInfo']
        # Parsing

        if 'authors' in item_info:
            authors = item_info['authors']
        else:
            authors = ''

        if 'categories' in item_info:
            categories = item_info['categories']
        else:
            categories = ""

        if 'title' in item_info:
            title = item_info['title']
            if 'subtitle' in item_info:
                title += ' '+ item_info['subtitle']
        else:
            title = ""

        if 'publishedDate' in item_info:
            published_date = item_info['publishedDate']
        else:
            published_date = ""

        if 'imageLinks' in item_info:
            img_link = item_info['imageLinks']['smallThumbnail']
            # img_link = item_info['imageLinks']['thumbnail']

            
        else:
            img_link = ""


        ISBN_10 = ''
        ISBN_13 = ''

        if 'industryIdentifiers' in item_info:
            identifiers = item_info['industryIdentifiers']
            for iden in identifiers:
                if iden['type'] == 'ISBN_13':
                    ISBN_13 = iden['identifier']
                elif iden['type'] == 'ISBN_10':
                    ISBN_10 = iden['identifier']
        else:
            identifiers = ''

        if "canonicalVolumeLink" in item_info:
            purchase_link = item_info["canonicalVolumeLink"]
        else:
            purchase_link = ''

        obj = {
            "categories" : categories,
            "title": title,
            "published_date" : published_date,
            'authors': authors,
            "img_link": img_link,
            'ISBN_13': ISBN_13,
            'ISBN_10': ISBN_10,
            "purchase_link": purchase_link
        }
        books_list.append(obj)

    return books_list

# print(search_book(sys.argv[1]))
# print(sys.argv[0])
# print(sys.argv[1])



