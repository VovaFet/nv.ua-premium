import sqlite3
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen

from numpy import full


def open_main_page():
    url = "https://nv.ua/premium.html"
    all_news_hrefs_list = []

    req = urlopen(url)
    soup = BeautifulSoup(req, "lxml")
    abs_href = soup.find_all(class_="absolute_link")
    all_img_links = soup.find_all("a", class_="atom-wrapper-body")
    all_journ_links = soup.find_all("a", class_="atom-text normal-text")
    all_additional_news_links = soup.find_all("a", class_="text")

    all_news_hrefs_list = extract_links(abs_href) + \
    extract_links(all_img_links) + extract_links(all_journ_links) + \
    extract_links(all_additional_news_links)

    return all_news_hrefs_list


def extract_links(links):
    ret_list = []
    for link in links:
        ret_list.append(link.get("href"))
    return ret_list


def db_init(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS articles(
        title TEXT,
        text TEXT,
        author TEXT,
        date_published TEXT,
        date_modified TEXT,
        link TEXT);""")
    conn.commit()
    return conn


def parse_link(link):
    soup = BeautifulSoup(urlopen(link), "lxml")

    for elem in soup.find_all("script", type="application/ld+json"):
        json_string = elem.text.strip()

    json_text_tag = json.loads(json_string)[3]

    try:
        article_title = json_text_tag['headline']
    except KeyError:
        article_title = None

    try:
        article_author = json_text_tag['author']['name']
    except KeyError:
        article_author = None

    try:
        atricle_text = json_text_tag['articleBody'].replace('Републикация полной версии запрещена', ' ').replace('Присоединяйтесь к нашему телеграм-каналу Мнения НВ',' ')
    except KeyError:
        article_text = None

    try:
        article_date_published = json_text_tag['datePublished']
    except KeyError:
        article_date_published = None

    try:
        article_date_modified = json_text_tag['dateModified']
    except KeyError:
        article_date_modified = None

    return [article_title, atricle_text, article_author, article_date_published, article_date_modified, link]


def commit_to_db(db_handler, row):
    cur = db_handler.cursor()
    cur.execute("INSERT INTO articles VALUES(?, ?, ?, ?, ?, ?);", row)
    db_handler.commit()


if __name__ == "__main__":

    links_list = open_main_page()
    print("Total articles num: ", len(links_list))
    db_handler = db_init('articles.db')

    for link in links_list:
        db_row = parse_link(link)
        commit_to_db(db_handler, db_row)
