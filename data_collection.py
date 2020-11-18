import os
from bs4 import BeautifulSoup
import re
import datetime
import csv
from langdetect import detect
import io

month_to_number = {'January': 1,
                   'February': 2,
                   'March': 3,
                   'April': 4,
                   'May': 5,
                   'June': 6,
                   'July': 7,
                   'August': 8,
                   'September': 9,
                   'October': 10,
                   'November': 11,
                   'December': 12}


def parse_html_in_folder(path):
    for html_file in os.listdir(path):
        with open(path + '/' + html_file, encoding='utf8') as infile:
            print(html_file)
            soup = BeautifulSoup(infile, features="lxml")
            # Plot can be hidden (if it is hidden we have to take the complete plot)
            try:
                Plot = ' '.join([c for c in soup.find_all('div',
                                                          id="description")[0].contents[3].contents if
                                 isinstance(c, str)])
            except:
                Plot = ' '.join([c for c in soup.find_all('div',
                                                          id="description")[0].contents[1].contents if
                                 isinstance(c, str)])
            if detect(Plot) != 'en':
                continue
            bookTitle = soup.find_all('h1')[0].contents[0].replace('\n', '').strip()
            bookSeries = soup.find_all('h2', id='bookSeries')[0].text.replace('\n', '').strip()
            bookAuthors = ', '.join([soup.find_all('span', itemprop='name')[i].contents[0] for i in range(
                len(soup.find_all('span', itemprop='name')))])
            ratingValue = soup.find_all('span', itemprop='ratingValue')[0].contents[0].replace('\n', '').strip()
            ratingCount = soup.find_all('meta', itemprop="ratingCount")[0]['content']
            reviewCount = soup.find_all('meta', itemprop="reviewCount")[0]['content']
            NumberofPages = re.findall(r'\d+', soup.find_all('span', itemprop="numberOfPages")[0].contents[0])[0]
            # Shall we remove the parenthesis? (e.g 'Portia (hunger Games)')
            temp_date = soup.find_all('div', id='details')[0].find_all('div', {"class": "row"})[1].text.split('\n')[
                2].split()
            PublishingDate = ' '.join(temp_date)
            # try:
            #     PublishingDate = datetime.datetime(int(temp_date[2]),
            #                                        month_to_number[temp_date[0]],
            #                                        int(re.findall(r'\d+', temp_date[1])[0]))
            # except:
            #     PublishingDate = datetime.datetime(int(temp_date[1]),
            #                                        month_to_number[temp_date[0]])
            characters = []
            settings = []
            for i in range(1, len(soup.find_all('div', id="bookDataBox")[0].find_all('a'))):
                if re.match(r'/characters/', soup.find_all('div', id="bookDataBox")[0].find_all('a')[i].attrs['href']):
                    characters.append(soup.find_all('div', id="bookDataBox")[0].find_all('a')[i].text)
                elif re.match(r'/places/', soup.find_all('div', id="bookDataBox")[0].find_all('a')[i].attrs['href']):
                    settings.append(soup.find_all('div', id="bookDataBox")[0].find_all('a')[i].text)
            characters = ', '.join(characters)
            settings = ', '.join(settings)
            url = soup.find_all('link', rel='canonical')[0].attrs['href']

            final_list = [bookTitle, bookSeries, bookAuthors, ratingValue, ratingCount, reviewCount,
                          Plot, NumberofPages, PublishingDate, PublishingDate, characters, settings, url]

            with io.open('data/tsv_files/book' + re.findall(r'\d+', html_file)[0] + '.tsv', 'wt',
                         newline='', encoding="utf-8") as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(final_list)
