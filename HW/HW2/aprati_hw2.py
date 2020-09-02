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

for k in range(1, 5): #want first four pages of petitions, page index starts at 1
    time.sleep(random.uniform(0, 5)) #building in pauses
    
    base_url = url + str(k)
    print(base_url)
    
    query = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(query.read(), features="lxml")
    soup.prettify()
    
    # find titles
    print("Parsing titles")
    titleList = soup.find_all('h3')
    
    for h in range(3, len(titleList)): #first three h3 are not titles
        titles.append(str(titleList[h]).split('</a>')[0].split('>')[2])
    
    # find "issues" (the tags for the petitions)
    # NB not every petition has issues! 
    print("Parsing issues")
    nodePetition = soup.find_all('article', {'class' : "node-petition"})
    
    for i in range(0, len(nodePetition)): #iterating over cards
        issueList = nodePetition[i].find_all('div', {'class' : "field-items"})
        if not issueList: #if there are no issues to append
            issues.append(["NA"])
        else: #if there are issues to append
            issueCount = len(issueList[0].find_all('h6')) #how many tags for each campaign?
            
            issueSubList = [] #adding tags as lists within the list
            for j in range(issueCount):
                issueSubList.append(str(issueList[0].find_all('h6')[j])
                                    .split('</h6>')[0].split('<h6>')[1])
            issues.append(issueSubList)
    
    # find number of signatures
    print("Parsing signatures")
    signatureList = soup.find_all('span', {'class' : "signatures-number"})
    
    for m in range(len(signatureList)):
        signatures.append(str(signatureList[m]).split('</span>')[0]
                          .split('<span class="signatures-number">')[1])
    
    # find published date - have to navigate into the page
    print("Parsing published dates")
    urlList = soup.find_all('a')
    
    base_url2 = "https://petitions.whitehouse.gov"
    
    # the first 12 and last 15 "a" tags are not petition urls
    for i in range(12, len(urlList)-15): #want every other url, otherwise have repeats
        time.sleep(1) # waiting for 1 second
        if i % 2 == 0: 
            subURL = base_url2 + str(urlList[i]).split('"')[1]
            query2 = urllib.request.urlopen(subURL)
            soup2 = BeautifulSoup(query2.read())
            soup2.prettify()
            metaData = soup2.find_all('h4', {'class' : "petition-attribution"})
            date = str(metaData).split('on ')[1].split('</h4>')[0]
            dates.append(date)
        else:
            continue

#want to ensure lists are of same length to match up
if len(titles)==len(issues)==len(signatures)==len(dates): 
    #creating a filename with a date and time stamp, since petitions change
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)
    filename = "hw2_output_" + timestamp + ".csv"
    print(filename)
    
    # writing to a csv
    # ANSI encoding removed some odd characters
    with open(filename, "w", encoding="ANSI", newline="",) as f:
      my_writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',')
      my_writer.writerow(["Title", "Published Date", "Issues", "Number of signatures"])
      for i in range(len(titles)):
         # write to csv one row at a time
         # for issues (the list within list), removes the [] and replaces with readable & sign
         row = [titles[i], dates[i], str(issues[i])[1:-1].replace("&amp;", "&"), signatures[i]]
         my_writer.writerow(row)
else:
    print("Unequal list lengths, check for errors:")
    print("Number of titles: " + str(len(titles)))
    print("Number of issues: " + str(len(issues)))
    print("Number of signatures: " + str(len(signatures)))
    print("Number of dates: " + str(len(dates)))