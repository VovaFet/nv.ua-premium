
def parsing_json(url):
  count_of_articles = 0
  for url in all_news_hrefs_list:
      soup_for_JSON = BeautifulSoup(urlopen(url), "lxml")  #готовим soup'чик
      script = soup_for_JSON.find_all('script', type='application/ld+json')
      for text_script in script:
          text_script = text_script.text.strip()
          count_of_articles += 1
          text_script = json.loads(text_script)[3] #выбираем нужный нам словарь из списка, (json.loads принимает объект и возвращает(преобразовывает) json объект в python dict)
          full_article = text_script['articleBody']#берём полную статью
          print(f"{count_of_articles}.{full_article}")

for url in list:
    parsing_json(url)