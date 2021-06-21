import requests
import csv
import json
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


def parse_huds(page_number):
    url = HUDS_PAGES_SWITCH_LINK + str(page_number)
    html = get_page(url)

    result = []
    soup = BeautifulSoup(html, "html5lib")
    containers = soup.find_all('div', class_='huds-directory')
    for i in containers:
        name = i.find('p', class_='huds-directory-item-name').text.strip()
        author = i.find('p', class_='huds-directory-item-user').text.strip()
        platforms_elem, ratios_elem = i.find_all('ul', class_='huds-directory-compatibility')

        supported_platforms = []
        for j in platforms_elem.find_all('li', class_='huds-directory-chip btn-check'):
            supported_platforms.append(j.text)

        aspect_ratio = []
        for j in ratios_elem.find_all('li', class_='huds-directory-chip btn-check'):
            aspect_ratio.append(j.text)

        links = i.find('div', class_='huds-directory-add-buttons').find_all('a')
        full_link = 'https://huds.tf/site/' + links[0]['href']
        download_link = 'https://huds.tf/site/' + links[1]['href']

        # Get the preview picture
        preview_img = 'https://huds.tf/site/' + i.find('img', class_='huds-directory-image img-fluid')['src']

        # Get the other pictures
        html1 = get_page(full_link)
        soup1 = BeautifulSoup(html1, 'html5lib')
        images = [preview_img]
        for j in soup1.find_all('div', class_='carousel-item'):
            images.append('https://huds.tf/site/' + j.find('img')['src'])

        result.append((name, author, supported_platforms, aspect_ratio, full_link, download_link, images))
    return result


def write_sound_db(db: list, db_type):
    with open(db_type + '.csv', 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'author', 'link'])
        for i in db:
            writer.writerow(i)


def write_hud_db(db: list):
    with open('huds.json', 'w') as f:
        json.dump(db, f)


def main():
    # Uncomment what you want to process

    # Sounds
    # sounds_list = []
    # for i in range(1, 51):  # 101 pages
    #     sounds_list += parse_sounds(i)
    #     print('Parsing... Current page ' + str(i))
    # write_sound_db(sounds_list, 'sounds')

    # HUDs
    huds_list = []
    for i in range(1, 7):
        huds_list += parse_huds(i)
        print('Parsing... Current page ' + str(i))

    write_hud_db(huds_list)


if __name__ == '__main__':
    main()
