import textwrap

import bs4
import requests
import datetime as dt
import os

default = os.path.join(os.curdir, "log.txt")


def logger(path=default):
    def decorator(old_function):
        def new_function(*args, **kwargs):
            old_res = old_function(*args, **kwargs)
            with open(path, 'a') as log_file:
                current_dt = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                log_entry = f'>> {current_dt}: '\
                            f'Called <{old_function.__name__}{args}>\n'\
                            f'--- result:\n'
                if old_res:
                    if isinstance(old_res, list):
                        result = old_res
                    else:
                        result = textwrap.fill(
                            old_res,
                            width=80,
                            initial_indent='---- ',
                            subsequent_indent='---- ')
                else:
                    result = '---- Нет результата'
                log_file.writelines(log_entry + result.strip() + '\n')
            return old_res

        return new_function

    return decorator

@logger()
def habr_article_parser(filter_word_list, mode):
    @logger()
    def words_search():
        if any([filter_word in article_text for filter_word in filter_word_list]):
            art_date = article.find('time').attrs.get('title')[:10]
            art_title = article.find('a', class_='tm-article-snippet__title-link').find('span').text
            art_href = url + article.find('a', class_='tm-article-snippet__title-link').attrs.get('href')
            search_result = f"<{art_date}> - <{art_title}> - <{art_href}>"
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
    print(results)
