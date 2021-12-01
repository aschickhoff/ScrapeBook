import requests
from bs4 import BeautifulSoup
import csv
import os

main_url = "https://books.toscrape.com/"

current_directory = os.getcwd()
work_directory = current_directory + "/AllBooks"
if not os.path.exists(work_directory):
    os.makedirs(work_directory)

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
    links = [main_url + "catalogue" + bl.find("a")["href"].split("..")[3] for bl in ltb]

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
        info_img_url = main_url  + soup2.find("div", id="product_gallery").find("img")["src"].split("..")[2]

        with open(current_directory + "/" + cat_names[n] + "_books.csv", "a", newline="", encoding="utf-8-sig") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([books, info_upc, info_title, info_including_tax, info_excluding_tax,
                                info_number_available, info_product_description, info_category,
                                info_rating, info_img_url])


        with open(current_directory + "/" + info_upc + ".jpg", "wb") as f:
            im = requests.get(info_img_url)
            f.write(im.content)

        print("Extracted information from book: " + info_title)


page = requests.get(main_url)
soup = BeautifulSoup(page.content, "html.parser")

categories = soup.find("ul", class_="nav nav-list").find_all("a")[1:]
cat_names = []
cat_links = []
for i in categories:
    cat_names.append(i.text.strip())
    cat_links.append(main_url + i["href"])

x = range(len(cat_names))
for n in x:
    current_directory = work_directory + "/" + cat_names[n]

    if not os.path.exists(current_directory):
        os.makedirs(current_directory)

    with open(current_directory + "/" + cat_names[n] + "_books.csv", "w", newline="", encoding="utf-8-sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["product_page_url", "universal_product_code (upc)", "title",
                             "price_including_tax", "price_excluding_tax", "number_available",
                             "product_description", "category", "review_rating", "image_url"])


    amount_of_pages = check_for_more_pages(cat_links[n])

    if amount_of_pages == "1":
        store_book_information(cat_links[n])
    else:
        for i in range(2, int(amount_of_pages)+2):
            store_book_information(cat_links[n])
            if i == 2:
                cat_links[n] = cat_links[n].replace("index.html", "page-" + str(i) + ".html")
            else:
                cat_links[n] = cat_links[n].replace("page-" + str(i-1) + ".html", "page-" + str(i) + ".html")
