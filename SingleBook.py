import requests
from bs4 import BeautifulSoup
import csv
import os


base_url = "https://books.toscrape.com/"
url = "https://books.toscrape.com/catalogue/the-natural-history-of-us-the-fine-art-of-pretending-2_941/index.html"
page = requests.get(url).text
soup = BeautifulSoup(page, "html.parser")

info_upc = soup.find("div", id="content_inner").find_all("td")[0].text
info_title = soup.find("div", id="content_inner").find_all("h1")[0].text
info_including_tax = soup.find("div", id="content_inner").find_all("td")[3].text.replace('Â', '')
info_excluding_tax = soup.find("div", id="content_inner").find_all("td")[2].text.replace('Â', '')
info_number_available = soup.find("div", id="content_inner").find_all("td")[5].text.split()[2].replace("(", "")
info_product_description = soup.find("div", id="content_inner").find_all("p")[3].text
info_category = soup.find("body", id="default").find_all("a")[3].text
info_rating = soup.find("div", id="content_inner").find_all("p")[2]["class"][1]
info_img_url = base_url  + soup.find("div", id="product_gallery").find("img")["src"].split("..")[2]



current_directory = os.getcwd()
work_directory = current_directory + "/SingleBook"
if not os.path.exists(work_directory):
	os.makedirs(work_directory)

with open(work_directory + "/single_book.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter = ',')
    csv_writer.writerow(["product_page_url", "universal_product_code (upc)", "title",
                         "price_including_tax", "price_excluding_tax", "number_available",
                         "product_description", "category", "review_rating", "image_url"])

    csv_writer.writerow([url, info_upc, info_title, info_including_tax, info_excluding_tax,
                         info_number_available, info_product_description, info_category,
                         info_rating, info_img_url])

print("Extracted information from book: " + info_title)