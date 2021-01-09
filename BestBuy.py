import requests
import json
from dataclasses import dataclass

@dataclass
class Item:
        name: str
        reg_price: float
        discount_price: float
        percent_off: float

def partition(list, start, end):
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

def quick_sort(list, start, end):
    if start >= end:
        return
    p = partition(list, start, end)
    quick_sort(list, start, p-1)
    quick_sort(list, p+1, end)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
response = requests.get("https://www.bestbuy.ca/api/v2/json/sku-collections/17056?categoryid=&currentRegion=BC&include=facets%2C%20redirects&lang=en-CA&page=1&pageSize=24&path=&query=&exp=&sortBy=relevance&sortDir=desc",headers=headers)
json_collection = json.loads(response.text)
num_pages = int(json_collection['totalPages'])
items_per_page = int(json_collection['pageSize'])
total_items = int(json_collection['total'])
item_list = []


for page in range(1, num_pages+1):
    url = f'https://www.bestbuy.ca/api/v2/json/sku-collections/17056?categoryid=&currentRegion=BC&include=facets%2C%20redirects&lang=en-CA&page={page}&pageSize=24&path=&query=&exp=&sortBy=relevance&sortDir=desc'
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    if(page == num_pages):
        for i in range(1, total_items - ((num_pages-1) * items_per_page) + 1):
            name = json_data['products'][i-1]['name']
            reg_price = float(json_data['products'][i-1]['regularPrice'])
            discount_price = float(json_data['products'][i-1]['salePrice'])
            percent_off = 1 - discount_price / reg_price
            item_list.append(Item(name, reg_price, discount_price, percent_off))
    else:
        for i in range(1, items_per_page+1):
            name = json_data['products'][i-1]['name']
            reg_price = float(json_data['products'][i-1]['regularPrice'])
            discount_price = float(json_data['products'][i-1]['salePrice'])
            percent_off = 1 - discount_price / reg_price
            item_list.append(Item(name, reg_price, discount_price, percent_off))

quick_sort(item_list, 0, len(item_list) - 1)
for i in range(0, len(item_list)):
    print("Product Name:", item_list[i].name)
    print("Regular Price:", '${:,.2f}'.format(item_list[i].reg_price), "Discounted Price:", '${:,.2f}'.format(item_list[i].discount_price), "Percent off:", str(int(100 * item_list[i].percent_off))+'%')
    print("\n")
