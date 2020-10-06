import requests
import urllib
import xml.etree.ElementTree as ET
from prettytable import PrettyTable
# Imports of libraries

#------!!!! YOU MUST PUT YOUR API KEY INSIDE KEY.TXT FILE !!!!------#
with open('key.txt', 'r') as file: #Read API key from key.txt
    key = file.read().replace('\n', '')

main_api = "https://www.goodreads.com/search.xml?" #The URL where API calls can be made.

# key = "YOUR_KEY_GOES_HERE" #My Private API Key #old and unsecure paintext

q = "" #Initialization of variable "q" holding user input.


titels = [] #Init of titels array.
authors = [] #Init of authors array.
avg_rating = [] #Init avg_rating array.
book_id = [] #Init book_id array.

while True:
    q = input("Book Name: ") #Ask user for input and store in variable q.
    if q == "quit" or q == "q": #if user input equals q or quit.
        break #stop 

    url = main_api + urllib.parse.urlencode({"key": key,"q": q}) #Add our private API key to the url to allow for API usage followed by the user's search query.
    print("URL: " + (url)) #Print the URL returned by API search query.

    r = requests.get(url) #send a get request to the API url.
    root = ET.fromstring(r.content) #Init root of tree from API url content.

    for results in root.findall(".//search/*"): #Search for any element within 'search'.
        for total in results.iter('total-results'): #Iterate over fields containing 'total_results'.
            if total.text == "0": #If the total results are 0.
                print("No books were found for",q+"!") #Print that there are no results found.
            else:

                print("The following books were found containing",q+".") #Print a message showing the user's search query.

                for f in root.findall(".//work/*"): #Search for any element within 'work'.
                    for rate in f.iter('average_rating'): #Iterate over fields containing 'average_rating'.
                        avg_rating.append(rate.text) #Add these to teh avg_rating array.

                for elem in root.findall(".//best_book/*"): #Search for any element within 'best_book'.
                    for title in elem.iter('title'): #Iterate over fields containing 'title'.
                        titels.append(title.text) #Add these to the titels array.
                
                for elem in root.findall(".//best_book/*"): #Search for any element within 'best_book'.
                    for bookid in elem.iter('id'): #Iterate over fields containing 'id' within 'best_book'.
                        book_id.append(bookid.text) #Add these to the book_id array.

                for author in root.findall(".//best_book/author/*"): #Search for anything within "best_book/author".
                    for author2 in author.iter('name'): #Iterate over fields containing 'name' within 'best_book/author'.
                        authors.append(author2.text) #Add these to the authors array.
                
                output = PrettyTable() #Init PrettyTable.
                output.field_names = ["Rating","Title","Book ID","Author"] #Append PrettyTable field names.
                
                for title,bid,author,rating in zip(titels,book_id,authors,avg_rating): #Iterate over arrays
                    output.add_row([rating,title,bid,author]) #Add the data from Arrays to rows.
                print(output) #Print the table with current data.

                output.clear_rows() #Clear the data added to rows.
                titels = [] #Clear all titles for previous search.
                authors = [] #Clear all authors for previous search.
                avg_rating = [] #Clear all ratings for previous search.
                book_id = [] #Clear all book ID's for previous search.





