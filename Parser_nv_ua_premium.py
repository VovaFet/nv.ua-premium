from bs4 import BeautifulSoup
import json
from urllib.request import urlopen

url = "https://nv.ua/premium.html"
#описываем заголовки get запроса
headers = {
"Accept": "*/*",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}
#выполняем get запрос страницы
req = urlopen(url)
# src = req.text
# # print(src)
#сохраняем html
# with open("index.html", "w") as file:
#     file.write(src)
#открываем в случае сохранения
# with open("index.html") as file:
#     src = file.read()
soup = BeautifulSoup(req, "lxml")
#создаём список ссылок всех новостей
all_news_hrefs_list = []
#забираем ссылку главной новости
abs_href = soup.find_all(class_="absolute_link")
for link in abs_href:
    link_href = link.get("href")
    all_news_hrefs_list.append(link_href)
#собираем ссылки со всех картинок новостей
all_img_links = soup.find_all("a", class_="atom-wrapper-body") #!!!!список ссылок из class_="atom-wrapper-body"
all_journ_links = soup.find_all("a", class_="atom-text normal-text") #список ссылок из class_="atom-text normal-text"
all_additional_news_links = soup.find_all("a", class_="text") #список ссылок дополнительных динамических новостей
for links in all_journ_links: #достаём ссылки atom-text normal-text из списка
    journ_links = links.get("href")
    all_news_hrefs_list.append(journ_links)

for links in all_img_links: #достаём ссылки atom-wrapper-body из списка
    img_links = links.get("href")
    all_news_hrefs_list.append(img_links)

for links in  all_additional_news_links:#достаём ссылки из "a", class_="text"
    additional_news_links = links.get("href")
    all_news_hrefs_list.append(additional_news_links)

print(len(all_news_hrefs_list))
print(all_news_hrefs_list)
#-------------------------------------<<<парсим JSON>>>---------------------------------------------------
count_of_articles = 0
for url in all_news_hrefs_list:
    src = url
    soup_for_JSON = BeautifulSoup(urlopen(src), "lxml")  #готовим soup'чик
    script = soup_for_JSON.find_all('script', type='application/ld+json')
    for text_script in script:
        text_script = text_script.text.strip()
        count_of_articles += 1

        text_script = json.loads(text_script)[3] #выбираем нужный нам словарь из списка, json.load принимает объект и возвращает(преобразовывает) json объект
        full_article = text_script['articleBody']#берём полную статью
        print(f"{count_of_articles}.{full_article}")
#-------------------------------------<<<заканчиваем парсить JSON>>>---------------------------------------------------
