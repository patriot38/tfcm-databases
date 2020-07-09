import requests
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
SOUND_PAGES_SWITCH_LINK = 'https://huds.tf/forum/forumdisplay.php?fid=27&page='
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
    containers = soup.find_all('div', class_='card text-theme bg-theme mb-3')

    result = []

    for i in containers:
        author_line = i.find('a', href=True, title=True)
        if not author_line:
            continue
        title = author_line['title']
        author = i.find('a', href=True, title=False).get_text()
        file_name = i.find('audio')['src']
        link = 'https://huds.tf/forum/' + file_name

        res = {'title': title,
               'author': author,
               'link': link}
        result.append(res)

    return result


def write_db(db: list, db_type):
    with open(db_type + '.xml', 'w') as file:
        file.write('<db></db>')
    tree = et.parse(db_type + '.xml')
    root = tree.getroot()
    iterator = 0
    for i in db:
        iterator += 1
        new_element = et.SubElement(root, 'sound' + str(iterator))
        new_element.set('title', i['title'])
        new_element.set('author', i['author'])
        new_element.set('link', i['link'])
    tree.write(db_type + '.xml')


def main():
    # Sounds
    sounds_list = []
    for i in range(1, 101):  # 101 pages
        sounds_list += parse_sounds(i)
        print('Parsing... Current page ' + str(i))
    write_db(sounds_list, 'sounds')

    # HUDs
    pass


if __name__ == '__main__':
    main()