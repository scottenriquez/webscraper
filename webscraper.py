# Web Scraper
import urllib as urllib2
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import time

app = Flask(__name__)

tu_base_url = "http://resources.utulsa.edu/schedule/2016FATUSCHED.html"
tu_url = "http://resources.utulsa.edu/schedule/2016FACS.html"
base_url = "http://resources.utulsa.edu/schedule/"
majors_url = "https://utulsa.edu/degrees/"

def download_html(url):
    response = urllib2.request.urlopen(url)
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

#Major Names
def major_names(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.find_all('td')
    major = []
    for row in table_rows[:76]:
        for a in row.find_all('a'):
            major.append(a.text)

    return major[:76]

#Disciplines
def scrape_disciplines(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.find_all('td')
    count = 0
    disciplines = []
    for row in table_rows[1:]:
        for a in row.find_all('a', href=True):
            disciplines.append(a['href'])
    return disciplines[:76]


def main():
    #html = download_html(tu_url)
    everything = []
    count = 0
    base_html = download_html(tu_base_url)
    major_names(base_html)
    print (major_names(base_html))
    urls_endings = scrape_disciplines(html)
    for end in urls_endings:
        print(base_url + end)
        html = download_html(base_url + end)
        #print html
        count = count + 1
        print("COUNT ", count)
        courses = scrape_courses(html)
        #everything.append(courses)
        #print courses
    #print everything

#def print_disciplines():


#@app.route('/')
#def index():
    #html = download_html(majors_url)
    #print scrape_courses(html)
#    main()
#    return render_template('layout.html')

@app.route('/index')
def get_data():
    html = download_html(tu_base_url)
    majors = major_names(html)
    return render_template("layout.html",majors=majors)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'GET':
        html = download_html(tu_base_url)
        majors = major_names(html)
        urls_endings = scrape_disciplines(html)
        result = {}
        for end in urls_endings:
            print(base_url + end)
            html = download_html(base_url + end)
            #print html
            courses = scrape_courses(html)
            for i, major in enumerate(majors):
                result[i] = courses[i]

        print(result)
    result = request.form
    return render_template("result.html",result = result)

if __name__ == '__main__':
    app.run(debug=True)
