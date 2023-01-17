import requests
from bs4 import BeautifulSoup
import os
import time
import json
from datetime import datetime
import csv
from lxml import html

#url_for_example = https://hard.rozetka.com.ua/computers/c80095/page=1;seller=rozetka/

def get_all_pages():
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    # r = requests.get(url="https://hard.rozetka.com.ua/computers/c80095/seller=rozetka;/", headers=headers)
    #
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # with open("data/page_1.html", 'w', encoding='utf-8') as file:
    #     file.write(r.text)

    with open('data/page_1.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find('div', class_="pagination ng-star-inserted").find_all("a")[-2].text)

    for i in range(1, pages_count + 1):
        if i == 1:
            url = 'https://hard.rozetka.com.ua/computers/c80095/seller=rozetka/'
        else:
            url = f'https://hard.rozetka.com.ua/computers/c80095/page={i};seller=rozetka/'

        r = requests.get(url=url, headers=headers)

        with open(f"data/page_{i}.html", 'w', encoding='utf-8') as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count + 1

def collect_data(pages_count):
    with open("Computers.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Name",
                "Price"
            )
        )

    data = []
    for page in range(1, pages_count):
        with open(f'data/page_{page}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        computers = soup.find_all("li", class_="catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted")

        for index, computer in enumerate(computers):
            computer_name = computer.find("span", class_="goods-tile__title").text.strip()
            computer_price = computer.find("p", class_="ng-star-inserted").text.rstrip(" ₴")

            #print(f"Name-{computer_name}, Price-{computer_price}")

            data.append(
                {
                    'computer_name': computer_name,
                    'computer_price': computer_price
                }
            )

            with open("Computers.csv", 'a', newline='') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        computer_name,
                        computer_price
                    )
                )

    with open('Computers.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    pages_count = get_all_pages()
    collect_data(pages_count)


if __name__ == '__main__':
    main()