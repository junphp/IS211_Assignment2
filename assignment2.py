import argparse
import urllib2
import csv
import datetime
import logging
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="Enter url you want to download csv")
    args = parser.parse_args()

    url = args.url
    #url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'
    try:
        data = downloadData(url)
    except:
        print("Invaild URL")
        exit()
    else:
        personData = processData(data)
        id = input("Enter user ID: ")
        while True:
            if id <= 0:
                print("Invaild ID")
                exit()
            else:
                displayPerson(id,personData)
                main()

def downloadData(url):
    url = urllib2.urlopen(url)
    return url

def processData(data):
    personData = {}
    csvData = csv.reader(data)
    next(csvData, None)
    for x in csvData:
        id = x[0]
        try:
            birthday = datetime.datetime.strptime(x[2], "%m/%d/%Y").strftime('%d/%m/%Y')
            personData[id] = (x[1], birthday)
        except:
            logging.basicConfig()
            mylogger = logging.getLogger("assignment2")
            mylogger.setLevel(logging.ERROR)
            file_handler = logging.FileHandler('error.log')
            mylogger.addHandler(file_handler)
            mylogger.error('Error processing line #%s for ID #%s',x[0],id,)
    return personData

def displayPerson(id,personData):
    id = str(id)
    try:
        birthday = datetime.datetime.strptime(personData[id][1], "%m/%d/%Y").strftime('%Y-%m-%d')
        name = personData[id][0]
        print("Person #%s is %s with a birthday of %s"%(id,name,birthday))
    except:
        print("No user found with that id")

main()