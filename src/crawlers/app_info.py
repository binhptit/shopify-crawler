from typing import Dict
from bs4 import BeautifulSoup
import urllib.request
import bs4
import random
import time
import logging
from .utils import filter_string, keep_number
import requests

def crawl_informaion_app_reviews(app_name:str, proxy_pool, old_reviews) -> Dict:
    page_number = 1
    comments = []
    proxy = proxy_pool.get_proxy()

    number_of_comments = 0
    match_old_reviews = False

    while True:
        time.sleep(random.randint(2,4))
        url_comments = f"https://apps.shopify.com/{app_name}/reviews?page={page_number}"

        try:
            with requests.Session() as session:
                response = session.get(url_comments, proxies={'http': f"http://{proxy}"})
                page = response.text        

            if "Too many comments" in response.text:
                raise Exception("Too many comments")
            
        except Exception as e:
            time.sleep(5)

            page = urllib.request.urlopen(url_comments)
            print("Exception:", e)

        soup = BeautifulSoup(page, 'html.parser')
        try:
            web_data = soup.find('span', class_='tw-text-body-md tw-text-fg-tertiary')
            if not number_of_comments:
                number_of_comments = int(keep_number(web_data.text))
        except Exception as e:
            number_of_comments = 0

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

            if comment_dict in old_reviews:
                match_old_reviews = True
                break

            comments.append(comment_dict)

        if match_old_reviews:
            break

        if app_name == 'pagefly':
            print(f"{app_name}. Comments: {len(comments)}.")
        page_number += 1

    if not match_old_reviews and len(comments) < number_of_comments:
        print(f"Missing comments: {number_of_comments - len(comments)}")
    else:
        print(f"Comments: {len(comments)}. Good!")
        
    return comments

def crawl_information_app(app_name:str, proxy_pool) -> Dict:
    url = f"https://apps.shopify.com/{app_name}"

    # page = urllib.request.urlopen(url)
    proxy = proxy_pool.get_proxy()
    try:
        with requests.Session() as session:
            response = session.get(url, proxies={'http': f"http://{proxy}"})
            page = response.text        
        proxy_pool.put_proxy(proxy)

        if "Too Many" in str(page):
            raise AttributeError("Too Many Requests")
        
    except Exception as e:
        time.sleep(10)
        page = urllib.request.urlopen(url)
        print("Exception:", e)

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
        "comments": [],
        "image_urls": []
    }

    web_data = soup.find('h1')
    result["app_name"] = web_data.text.strip()
    web_data = soup.find('span', class_='tw-text-body-sm tw-text-fg-secondary')
    result["overall_rating"] = float(filter_string(web_data.text.strip(), '0123456789.'))
    web_data = soup.find('div',class_='tw-px-md xl:tw-px-lg tw-border-solid tw-border-x tw-border-stroke-primary').find('a')
    try:
        result["reviews"] = int(keep_number(web_data.text.strip()))
    except Exception as e:
        result["reviews"] = 0

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

    web_data = soup.find('div',class_="gallery-component__content").find_all('li')
    for result_set_data in web_data:
        try:
            result["image_urls"].append(result_set_data.find('img')['src'])
        except Exception as e:
            # logging.info(e, "image_urls in application crawling")
            continue
    
    web_data = soup.find_all('div',class_="gallery-component__item tw-aspect-[16/9] first:tw-ml-md last:tw-mr-md tw-snap-center tw-cursor-pointer tw-flex tw-justify-center tw-shadow-lg tw-mr-md tw-min-w-[80%] tw-bg-fg-primary tw-bg-clip-content tw-rounded-md")
    for result_set_data in web_data:
        try:
            result["image_urls"].append(result_set_data.find('img')['src'])
        except Exception as e:
            # logging.info(e, "image_urls in application crawling")
            continue

    return result