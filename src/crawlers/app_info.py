from typing import Dict
from bs4 import BeautifulSoup
import urllib.request
import bs4
import random
import time
import json
from .utils import filter_string

def crawl_informaion_app_reviews(app_name:str) -> Dict:
    page_number = 1
    comments = []
    while True:
        time.sleep(random.randint(0,1))
        url_comments = f"https://apps.shopify.com/{app_name}/reviews?page={page_number}"
        page = urllib.request.urlopen(url_comments)
        soup = BeautifulSoup(page, 'html.parser')
        web_data = soup.find_all('div',class_='tw-py-lg lg:tw-py-xl first:tw-pt-0 last:tw-pb-0')
        if not len(web_data):
            break
        for result_set_data in web_data:
            comment_dict = {
                "content": "",
                "date": "",
                "rate": 0
            }
            html_data = str(result_set_data)
            s = BeautifulSoup(html_data, "html.parser")
            div = s.find("div", attrs={"aria-label": True})
            string = str(div["aria-label"])
            split = string.split()
            comment_dict["rate"] = split[0]
            data = s.find('p',class_='tw-break-words')
            comment_dict["content"] = data.text.strip()
            data = s.find('div',class_='tw-text-body-xs tw-text-fg-tertiary')
            comment_dict["date"] = data.text.strip()
            
            comments.append(comment_dict)
        page_number += 1
    return comments

def crawl_information_app(app_name:str) -> Dict:
    url = f"https://apps.shopify.com/{app_name}"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    result = {
        "app_name": "",
        "overall_rating": 0.0,
        "reviews": 0,
        "developer": "",
        "highlights": [],
        "launched": "",
        "languages": "",
        "categories": [],
        "description": {
            "short": "",
            "long": "",
            "features": []
        },
        "ratings": [],
        "comments": []
    }

    web_data = soup.find('h1')
    result["app_name"] = web_data.text.strip()
    web_data = soup.find('span', class_='tw-text-body-sm tw-text-fg-secondary')
    result["overall_rating"] = float(filter_string(web_data.text.strip(), '0123456789.'))
    web_data = soup.find('div',class_='tw-px-md xl:tw-px-lg tw-border-solid tw-border-x tw-border-stroke-primary').find('a')
    result["reviews"] = int(web_data.text.strip())
    web_data = soup.find('div',class_='tw-pl-md xl:tw-pl-lg').find('a')
    result["developer"] = web_data.text.strip()
    web_data = soup.find('div','tw-col-span-full md:tw-col-span-4 lg:tw-col-span-3 tw-flex tw-flex-col tw-gap-xl').find('div',class_="").find_all('span')

    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            if result_set_data.text.strip():
                result["highlights"].append(result_set_data.text.strip())
    else:
        result["highlights"].append(web_data.text.strip())

    web_data = soup.find_all('p', class_="tw-text-fg-tertiary tw-text-body-sm")
    result["launched"] = web_data[0].text.strip()
    result["languages"] = web_data[1].text.strip()

    web_data = soup.find('span',class_="tw-text-fg-tertiary tw-text-body-sm").find_all('a')
    for item in web_data:
        result["categories"].append(item.text.strip())

    web_data = soup.find('h2',class_="tw-text-heading-4")
    result["description"]["short"] = web_data.text.strip()
    web_data = soup.find('p',class_="tw-hidden lg:tw-block tw-text-body-xl tw-text-fg-tertiary")
    result["description"]["long"] = web_data.text.strip()
    web_data = soup.find('div',class_="tw-flex tw-flex-col tw-gap-lg lg:tw-gap-xl").find('ul').find_all('span',class_="")
    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            result["description"]["features"].append(result_set_data.text.strip())
    else:
        result["description"].append(web_data.text.strip())

    web_data = soup.find('div',class_="app-reviews-metrics").find_all('span')
    for result_set_data in web_data:
        result_item = result_set_data.text.strip()
        if "%" in result_item:
            result["ratings"].append(result_set_data.text.strip())

    result["comments"] = crawl_informaion_app_reviews(app_name)

    return result

if __name__ == '__main__':
    app_slug =  "walmart-marketplace"
    crawl_result = crawl_information_app(app_slug)

    with open(f'data/{app_slug}.json', 'w') as outfile:
        json.dump(crawl_result, outfile, indent=4)