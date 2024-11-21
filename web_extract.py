import requests
from bs4 import BeautifulSoup
import csv
import json

# Get html page and return as BeautifulSoup object
def get_html(page):
    HEADERS = { 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    html_request = requests.get(page, headers=HEADERS)
    soup = BeautifulSoup(html_request.content, 'html.parser')
    
    return soup

# Retreive json file from a given url
def get_json(url):
    
    page = requests.get(url)
    data = page.json()
    
    return data

# Read in a csv file and output data in dictionary form
def csv_to_dict(filename):
    data = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            data[row[0]] = row[1]
            
    return data

# Read in a csv and output data in list form
def csv_to_list(filename):
    data = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        new_row = []
        for row in csvreader:
            if len(row) > 1:
                for item in row:
                    new_row.append(item)
                data.append(new_row)
            else:
                data.append(row)
                
    return data

# Write to csv file
# Input format: lists within a list [[],[],[],[]]
def write_csv(data, filename):
    # Opening/creating csv file for saving data
    with open(f'.\\Data\\{filename}.csv', 'w', newline='') as file: # newline='' stops from writing to every other row
        writer = csv.writer(file)
       
        # Iterating data to produce row in csv doc
        for row in data:
            # Writing row data to csv
            writer.writerow(row)

    print(f'{filename} CSV created')