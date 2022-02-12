import bs4
import requests


def habr_article_parser(filter_word_list, mode):

    def words_search():
        if any([filter_word in article_text for filter_word in filter_word_list]):
            art_date = article.find('time').attrs.get('title')[:10]
            art_title = article.find('a', class_='tm-article-snippet__title-link').find('span').text
            art_href = url + article.find('a', class_='tm-article-snippet__title-link').attrs.get('href')
            search_result = f"<{art_date}> - <{art_title[:30]}> - <{art_href}>"
            print('>>> Найдено совпадение')
            return search_result

    url = 'https://habr.com'
    rg = requests.get(url + '/ru/all')
    soup = bs4.BeautifulSoup(rg.text, 'html.parser')

    # Находим все статьи на странице
    articles = soup.find_all('article', class_='tm-articles-list__item')
    result = []

    if mode == 'preview':
        for article in articles:
            words = article.find_all('span')
            words += article.find_all('p')
            article_text = [word.text.lower().strip() for word in words]
            article_text = ' '.join(article_text)
            hit = words_search()
            if hit:
                result.append(hit)

    elif mode == 'detail':
        for article in articles:
            href = url + article.find('a', class_='tm-article-snippet__title-link').attrs.get('href')
            print(f'Обработка страницы {href}...')
            rg = requests.get(href)
            detail_page = bs4.BeautifulSoup(rg.text, 'html.parser')

            # with open("detail_index.html") as fp:
            #     detail_page = bs4.BeautifulSoup(fp, 'html.parser')

            content = detail_page.find('div', id='post-content-body').find_all('p')
            article_text = ''
            for paragraph in content:
                article_text += paragraph.text.strip().lower() + ' '
            hit = words_search()
            if hit:
                result.append(hit)
    else:
        print('Неверный параметр')
        exit(1)
    return result


if __name__ == '__main__':
    FILTER_WORDS = ['демоны', 'фото', 'web', 'python']
    # WORK_MODE = 'preview'  # Поиск слов в превью по главной странице
    WORK_MODE = 'detail'  # Поиск слов по полным статьям

    results = habr_article_parser(FILTER_WORDS, WORK_MODE)
    print('\nРезультаты поиска:')
    print(*results, sep='\n')


