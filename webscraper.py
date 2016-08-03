# Web Scraper
import urllib2
from bs4 import BeautifulSoup
from flask import Flask
import time

app = Flask(__name__)

tu_base_url = "http://resources.utulsa.edu/schedule/2016FATUSCHED.html"
tu_url = "http://resources.utulsa.edu/schedule/2016FACS.html"
base_url = "http://resources.utulsa.edu/schedule/"

def download_html(url):
    proxy = urllib2.ProxyHandler({'http': 'bvl-proxy1.conocophillips.net'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url)
    return response.read()

def scrape_courses(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.find('table').find_all('tr')
    courses = []
    for row in table_rows[1:]:
        table_data = row.find_all('td')
        course = {
            'Status' : table_data[0].text,
            'Course' : table_data[1].text,
            'Section' : table_data[2].text,
            'Title' : table_data[4].text,
            'Meeting Times' : table_data[5].text,
            'Instructor' : table_data[6].text
        }
        courses.append(course)
    return courses

def scrape_disciplines(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.find_all('td')
    count = 0
    disciplines = []
    for row in table_rows[1:]:
        for a in row.find_all('a', href=True):
            disciplines.append(a['href'])
            print a['href']
            count = count + 1
            #print count
            #time.sleep(1)
    return disciplines[:74]


def main():
    #html = download_html(tu_url)
    everything = []
    count = 0
    base_html = download_html(tu_base_url)
    urls_endings = scrape_disciplines(base_html)
    for end in urls_endings:
        print base_url + end
        html = download_html(base_url + end)
        #print html
        count = count + 1
        print "COUNT ", count
        courses = scrape_courses(html)
        everything.append(courses)
        #print courses
    #print everything

@app.route('/')
def index():
    main()
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)