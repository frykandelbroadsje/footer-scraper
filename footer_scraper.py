#!/usr/bin/python3
"""
Scrape the text from the footer of a website and put it in a dictionary.
Output into a json file
"""

__author__ = "Ype Zijlstra"
__email__ = "y.zijlstr@gmail.com"
__licence__ = "MIT"
__version__ = "1.0.1"
__status__ = "Production"


import json
import requests
import os
from bs4 import BeautifulSoup
from time import sleep


def scrape_footer(session: requests.Session = None, url: str = None) -> list:
    """
    Scrape the footers from a webpage given a url
    :param url: the url to the website
    :return: a list of all unique bodies of text in the footer
    """

    if session is None:
        with requests.Session() as session:
            website_html = session.get(url).text
    else:
        website_html = session.get(url).text

    soup = BeautifulSoup(website_html, 'html.parser')
    footer = soup.find('footer')

    divs = footer.find_all('div')

    text_list = list()
    # Loop through all 'div' elements in the footer
    for div in divs:
        # Only consider divs with text of length greater than 1
        if len(div.text.strip()) > 1:
            div_text = div.text.strip()
            # Split div text string along newline characters
            newline_list = div_text.split('\n')
            for n_item in newline_list:
                # Split newline items along carriage returns
                carriage_list = n_item.split('\r')
                for c_item in carriage_list:
                    # Only append text_list with string if string not in text_list yet
                    if c_item.strip() not in text_list:
                        if len(c_item.strip()) > 1:
                            # Only append text list with string if string length greater than 1
                            text_list.append(c_item.strip())

    return text_list


def collect_footers(url_list: list) -> dict:
    """
    Collect the footer text from a list of website given a list of urls
    :param urls: a list of urls to scrape
    :return a dictionary of urls with footer text of associated website
    """

    if not isinstance(url_list, list):
        url_list = [url_list]

    footer_dict = dict()
    with requests.Session() as session:
        for url in url_list:
            if not (url.startswith( 'http' )):
                url = "https://" + url
                print(url)
            try:
                footer_text = scrape_footer(session, url.strip())
                footer_dict.update({url: footer_text})
                print(f"Scraped url \'{url}\'.")
                sleep(1)
            except Exception as e:
                print(f"Could not scrape url \'{url}\'. Cause:")
                print(e)
                continue

    return footer_dict


if __name__ == '__main__':
    inputfile = open("domains.txt","r")
    web_designer_urls = inputfile.readlines()
    # web_designer_urls = ['https://www.studiospijker.nl/studio/',
    #                      'https://www.studioplakband.com/',
    #                      'https://nieteenechtewebdesigner.org/',
    #                      'https://dsignonline.nl/',
    #                      'https://www.convident.nl/',
    #                      'https://www.webnexus.nl/']

    web_designer_dict = collect_footers(web_designer_urls)

    # Print dictionary to console
    print(json.dumps(web_designer_dict, indent=4, ensure_ascii=False))

    # Write output to json file
    with open(f'{os.path.dirname(__file__)}/web_design_footers.json', 'w') as f:
        json.dump(web_designer_dict, f, indent=4, ensure_ascii=False)
