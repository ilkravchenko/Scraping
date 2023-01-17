import requests
from bs4 import BeautifulSoup
import os
import time
import json
from datetime import datetime
import csv


def get_all_pages():
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    # r = requests.get(url="https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/", headers=headers)
    #
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # with open("data/page_1.html", 'w') as file:
    #     file.write(r.text)

    with open("data/page_1.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find("div", class_="bx-pagination-container").find_all("a")[-2].text)

    for page in range(1, pages_count + 1):
        url = f"https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}"

        r = requests.get(url=url, headers=headers)

        with open(f"data/page_{i}.html", 'w') as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count + 1

def collect_data(pages_count):
    date_now = datetime.now().strftime("%d_%m_%y")

    with open(f"data_{date_now}.csv", 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Article",
                "Link",
                "Price"
            )
        )

    data = []
    for page in reange(1, pages_count):
        with open(f'data/page_{page}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        cards_of_watch = soup.find_all("a", class_="product-item__link")

        for card in cards_of_watch:
            product_article = item.find("p", class_="product-item__articul").text.strip()
            product_price = item.find("p", class_="product-item__price").text.lstrip("руб. ")
            product_url = f'https://shop.casio.ru{item.get("href")}'

            data.append(
                {
                    'product_article' : product_article,
                    'product_price': product_price,
                    'product_url': product_url
                }
            )

            with open(f"data_{date_now}.csv", 'a') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_article,
                        product_url,
                        product_price
                    )
                )

    with open(f'data_{date_now}.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    pages_count = get_all_pages()
    collect_data(pages_count)

if __name__ == '__main__':
    main()