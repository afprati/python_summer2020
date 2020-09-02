# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 13:47:08 2020

@author: miame
"""

"""
- Go to https://petitions.whitehouse.gov/petitions
- Go to the petition page for each of the petitions.
- Create a .csv file with the following information for each petition:
    - Title
    - Published date
    - Issues
    - Number of signatures
"""

from bs4 import BeautifulSoup
import urllib.request
import csv
import random
import time

url = 'https://petitions.whitehouse.gov/?page='
titles = []
dates = []
issues = []
signatures = []

for k in range(1,5):
    time.sleep(random.uniform(0, 3))
    base_url = url + str(k)
    print(base_url)
    
    query = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(query.read(), features="lxml")
    soup.prettify()
    
    # find titles
    titleList = soup.find_all('h3')
    #print(titleList)
    #print(titleList[3])
    
    for h in range(3, len(titleList)):
        titles.append(str(titleList[h]).split('</a>')[0].split('>')[2])
    
    #print(titles)
    
    # find "issues" (the tags for the petitions)
    issueList = soup.find_all('div', {'class' : "field-items"})
    #print(issueList)
    
    for i in range(1, len(issueList)):
        issueCount = len(issueList[i].find_all('h6')) #how many tags for each campaign?
        issueSubList = []
        for j in range(issueCount):
            issueSubList.append(str(issueList[i].find_all('h6')[j])
                                .split('</h6>')[0].split('<h6>')[1])
        issues.append(issueSubList)
        
    #print(issues)
    
    # find number of signatures
    signatureList = soup.find_all('span', {'class' : "signatures-number"})
    #print(signatureList)
    
    for m in range(len(signatureList)):
        signatures.append(str(signatureList[m]).split('</span>')[0]
                          .split('<span class="signatures-number">')[1])
    
    #print(signatures)
    
    
    # find published date - have to navigate into the page
    urlList = soup.find_all('a')
    #print(urlList)
    #print(urlList[12])
    #print(urlList[14])
    #print(urlList[51])
    
    base_url2 = "https://petitions.whitehouse.gov"
    
    for i in range(12, len(urlList)-15):
        time.sleep(random.uniform(0, 3))
        if i % 2 == 0: 
            #print(i)
            subURL = base_url2 + str(urlList[i]).split('"')[1]
            #print(subURL)
            query2 = urllib.request.urlopen(subURL)
            soup2 = BeautifulSoup(query2.read())
            soup2.prettify()
            metaData = soup2.find_all('h4', {'class' : "petition-attribution"})
            date = str(metaData).split('on ')[1].split('</h4>')[0]
            #print(date)
            dates.append(date)
        else:
            continue
        
    #print(dates)

# writing to a csv

with open("hw2_output.csv", "w", encoding="utf-8", newline="",) as f:
  my_writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',')
  my_writer.writerow(["Title", "Issues", "Number of signatures"])
  for i in range(len(titles)):
     row = [titles[i], issues[i], signatures[i]]
     my_writer.writerow(row)