import requests
from bs4 import BeautifulSoup
import csv
import os

base_url = "https://books.toscrape.com/"
url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"

current_directory = os.getcwd()
work_directory = current_directory + "/CategoryBook"
if not os.path.exists(work_directory):
    os.makedirs(work_directory)

with open(work_directory + "/category_books.csv", "w", newline="", encoding="utf-8-sig") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["product_page_url", "universal_product_code (upc)", "title",
                        "price_including_tax", "price_excluding_tax", "number_available",
                        "product_description", "category", "review_rating", "image_url"])

def check_for_more_pages(url_to_check):
    page = requests.get(url_to_check)
    soup = BeautifulSoup(page.content, "html.parser")
    check_for_amount_of_pages = soup.find('li', class_="current")
    if check_for_amount_of_pages != None:
        check_for_amount_of_pages = soup.find('li', class_="current").text.strip().split(" ")
        return check_for_amount_of_pages[-1]
    else:
        return 1

def store_book_information(current_url):
    page = requests.get(current_url).text
    soup = BeautifulSoup(page, "html.parser")
    ltb = soup.find_all("div", class_="image_container")
    links = [base_url + "catalogue" + bl.find("a")["href"].split("..")[3] for bl in ltb]

    for books in links:
        page2 = requests.get(books).text
        soup2 = BeautifulSoup(page2, "html.parser")

        info_upc = soup2.find("div", id="content_inner").find_all("td")[0].text
        info_title = soup2.find("div", id="content_inner").find_all("h1")[0].text
        info_including_tax = soup2.find("div", id="content_inner").find_all("td")[3].text.replace('Â', '').replace("Â", "")
        info_excluding_tax = soup2.find("div", id="content_inner").find_all("td")[2].text.replace('Â', '').replace("Â", "")
        info_number_available = soup2.find("div", id="content_inner").find_all("td")[5].text.split()[2].replace("(", "")
        info_product_description = soup2.find("div", id="content_inner").find_all("p")[3].text
        info_category = soup2.find("body", id="default").find_all("a")[3].text
        info_rating = soup2.find("div", id="content_inner").find_all("p")[2]["class"][1]
        info_img_url = base_url  + soup2.find("div", id="product_gallery").find("img")["src"].split("..")[2]

        with open(work_directory + "/category_books.csv", "a", newline="", encoding="utf-8-sig") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([url, info_upc, info_title, info_including_tax, info_excluding_tax,
                                info_number_available, info_product_description, info_category,
                                info_rating, info_img_url])

        print("Extracted information from book: " + info_title)


amount_of_pages = check_for_more_pages(url)

if amount_of_pages == "1":
    store_book_information(url)
else:
    for i in range(2, int(amount_of_pages)+2):
        store_book_information(url)
        if i == 2:
            url = url.replace("index.html", "page-" + str(i) + ".html")
        else:
            url = url.replace("page-" + str(i-1) + ".html", "page-" + str(i) + ".html")
