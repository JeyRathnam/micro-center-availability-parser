import requests
from bs4 import BeautifulSoup
import os
import re
from config import urls
import textwrap
import smtplib
import mail


def get_from_html(file_name):
    f = open(os.path.join(os.path.abspath(''),file_name), 'r')
    text =  f.read()
    f.close()
    return text

def extract_price(price_html):
    currency_sym = price_html.find("span", {"class" : "upper"}).string
    price = price_html.get("content")
    return currency_sym + price
    
    
def extract_inventory_count(inventory_html):
    msg_in_stock = inventory_html.find("span", {"class" : "msgInStock"})
    if msg_in_stock:
        msg_in_stock.decompose()
    inv_count_html = inventory_html.find("span", {"class" : "inventoryCnt"})
    if inv_count_html:
        return inv_count_html.text.strip()
    else:
        return 0

def extract_title(html):
    title = html.find("title").get_text()
    title = re.sub('\s+',' ',title)
    return title.strip()
    

def check_product_availability(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    title = extract_title(soup)

    price_html= soup.find("span", {"id" : "pricing"})
    price = extract_price(price_html)
    
    inventory_html = soup.find("p" , {"class": "inventory"})
    inventory = extract_inventory_count(inventory_html)
    
    is_available = "SOLD OUT" not in inventory_html

    return (is_available, inventory, price, title)


if __name__ == "__main__":
    cookies = {"storeSelected" : "131"}

    for url in urls:
        r = requests.get(url, cookies=cookies, timeout=10)
        html_text = r.text

        is_available, inventory, price, title = check_product_availability(html_text)

        if is_available:
            mail.send('Micro Center available - {}'.format(title), '{} - {} - {}'.format(title, price, inventory))




def test_available():
    with open(os.path.join(os.path.abspath(''), "available.html"), 'r') as f:
        html = f.read()
        test_res = check_product_availability(html)

        assert (True, '25+', '$499.99', 'HP Pavilion 15-eg0053cl 15.6\" Laptop Computer Refurbished - Silver; Intel Core i5 11th Gen 1135G7 2.4GHz Processor; - Micro Center') == test_res
    
def test_unavailable():
    with open(os.path.join(os.path.abspath(''), "unavailable.html"), 'r') as f:
        html = f.read()
        test_res = check_product_availability(html)
        assert (False, 0, '$1,299.99', 'ASUS NVIDIA GeForce RTX 3080 ROG Strix Gundam Edition Overclocked Triple-Fan 10GB GDDR6X PCIe 4.0 Graphics Card - Micro Center') == test_res