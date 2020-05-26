#Important import statements.
import requests 
import json
from dataclasses import dataclass

@dataclass
class Item: #This class represents an Item on the Sales Catalog. An Item has a name, regular price, regular price, and percent off. 
        name: str
        reg_price: float
        discount_price: float
        percent_off: float

def partition(list, start, end): #Simple Partition Function, where we are sorting the passed in List by percent_off. 
    pivot = list[start].percent_off
    low = start + 1
    high = end

    while True:
        while low <= high and list[high].percent_off >= pivot:
            high = high - 1
        while low <= high and list[low].percent_off <= pivot:
            low = low + 1
        if low <= high:
            list[low], list[high] = list[high], list[low]
        else:
            break
    list[start], list[high] = list[high], list[start]
    return high

def quick_sort(list, start, end): #With the partition function above, we can complete our quick-sort implmentation.
    if start >= end:
        return
    p = partition(list, start, end)
    quick_sort(list, start, p-1)
    quick_sort(list, p+1, end)

#response holds the first page of the Best Buy gaming sales catalog. 
response = requests.get("https://www.bestbuy.ca/api/v2/json/sku-collections/17056?categoryid=&currentRegion=BC&include=facets%2C%20redirects&lang=en-CA&page=1&pageSize=24&path=&query=&exp=&sortBy=relevance&sortDir=desc") 
#To make the page easier to work with, noticing it is in JSON format, I use the JSON library to store the page as a JSON collection that we can actually use. 
json_collection = json.loads(response.text)
#Collect constant variables, found through looking at the Page.  
num_pages = int(json_collection['totalPages'])
items_per_page = int(json_collection['pageSize'])
total_items = int(json_collection['total'])
item_list = []


for page in range(1, num_pages+1): #We loop starting at page 1, to the last page. 
    #To get the unique URL for each page, I use an f String which will update the url corresponding to the page variable.  
    url = f'https://www.bestbuy.ca/api/v2/json/sku-collections/17056?categoryid=&currentRegion=BC&include=facets%2C%20redirects&lang=en-CA&page={page}&pageSize=24&path=&query=&exp=&sortBy=relevance&sortDir=desc'
    #Format current Page to JSON. 
    response = requests.get(url)
    json_data = json.loads(response.text)
    #If the scraper is at the last page, 
    if(page == num_pages):
    #The last page may contain less items than the items_per_page, and so to account for that, we manually calculate the number of items on said page. 
        for i in range(1, total_items - ((num_pages-1) * items_per_page) + 1):
            #collect data, apply to type Item, and append to the list.  
            name = json_data['products'][i-1]['name']
            reg_price = float(json_data['products'][i-1]['regularPrice'])
            discount_price = float(json_data['products'][i-1]['salePrice'])
            percent_off = 1 - discount_price / reg_price
            item_list.append(Item(name, reg_price, discount_price, percent_off))
    else:
        for i in range(1, items_per_page+1):
            #collect data, apply to type Item, and append to the list. 
            name = json_data['products'][i-1]['name']
            reg_price = float(json_data['products'][i-1]['regularPrice'])
            discount_price = float(json_data['products'][i-1]['salePrice'])
            percent_off = 1 - discount_price / reg_price
            item_list.append(Item(name, reg_price, discount_price, percent_off))
         
#Sort List, and print to terminal.  
quick_sort(item_list, 0, len(item_list) - 1) 
for i in range(0, len(item_list)):
    print("Product Name:", item_list[i].name)
    print("Regular Price:", '${:,.2f}'.format(item_list[i].reg_price), "Discounted Price:", '${:,.2f}'.format(item_list[i].discount_price), "Percent off:", str(int(100 * item_list[i].percent_off))+'%')
