import requests
from utils import get_image_url
import csv


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.matchesfashion.com'
}


start_urls = [
    "https://api.matchesfashion.com/search?pageSize=72&channel=web&country=GBR&currency=GBP&gender=womens&language=en&pageOffset={}&url=%2Fwomens%2Fshop%2Fshoes&q=categories%3Acatalog01_womensshop_womensshoes&shoeSizeSystem=uksearch",
    "https://api.matchesfashion.com/search?pageSize=72&channel=web&country=GBR&currency=GBP&gender=mens&language=en&pageOffset={}&url=%2Fmens%2Fshop%2Fshoes&q=categories%3Acatalog01_mensshop_mensshoes&shoeSizeSystem=uksearch"
]


def start_requests(url):
    send_request = requests.get(
        url.format(0),
        headers=headers
    ).json()
    pagination = send_request.get("data").get("pagination")
    number_of_pages = pagination.get("numberOfPages")
    for page in range(0, number_of_pages+1):
        print(f"downloading {page+1} page from {number_of_pages+1}")
        yield requests.get(
            url.format(page),
            headers=headers
        ).json()


def parse(response):
    data = response.get("data")
    products = data.get("products")
    for product in products:
        yield product


def parse_details(product):
    title = product.get('basicInfo').get('name')
    url = product.get('basicInfo').get('productUrl')
    price = product.get('analytics').get('price')
    image_url = get_image_url(product)
    category = product.get('analytics').get('itemCategory3')
    gender = product.get('basicInfo').get('gender')
    # print(title, url, price, image_url, category, gender)
    # Write product details to a CSV file
    with open('products.csv', 'a', newline='') as csvfile:
        fieldnames = ['title', 'url', 'price', 'image_url', 'category', 'gender']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header row if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write product details to the CSV file
        writer.writerow({
            'title': title,
            'url': url,
            'price': price,
            "image_url": image_url,
            "category": category,
            "gender": gender
        })


if __name__ == "__main__":
    for url in start_urls:
        get_response = start_requests(url)
        for response in get_response:
            get_products = parse(response)
            for product in get_products:
                parse_details(product)
