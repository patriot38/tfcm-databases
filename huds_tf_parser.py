import requests
import csv
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
SOUND_PAGES_SWITCH_LINK = 'https://huds.tf/site/d-Hitsound?page='
HUDS_PAGES_SWITCH_LINK = 'https://huds.tf/forum/forumdisplay.php?fid=25&page='


def get_page(url):
    req = requests.get(url, headers=HEADERS)

    if req.status_code != 200:
        print("Oops! Couldn't get web page's source code!")
        exit(-1)

    return req.text


def parse_sounds(page_number):
    url = SOUND_PAGES_SWITCH_LINK + str(page_number)
    html = get_page(url)

    soup = BeautifulSoup(html, "html5lib")
    containers = soup.find_all('div', class_='huds-directory')

    result = []

    for i in containers:
        author_info = i.find('div', class_='huds-directory-lower')
        if not author_info:
            continue
        title = i.find('p', class_='huds-directory-item-name').find('a').text
        author = i.find('p', class_='huds-directory-item-user').text.strip()
        link = i.find('audio')['src']
        link = 'https://huds.tf/forum/' + link

        res = [title, author, link]
        result.append(res)

    return result


def write_db(db: list, db_type):
    with open(db_type + '.csv', 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'author', 'link'])
        for i in db:
            writer.writerow(i)


def main():
    # Sounds
    sounds_list = []
    for i in range(1, 51):  # 101 pages
        sounds_list += parse_sounds(i)
        print('Parsing... Current page ' + str(i))
    write_db(sounds_list, 'sounds')

    # HUDs
    pass


if __name__ == '__main__':
    main()