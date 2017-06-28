from bs4 import BeautifulSoup
from urllib import request

# title = input('Name of the Wikipedia page:\n')

title = 'Valkyrie'
# Convert to proper link
title = title.replace(' ', '_')


url = 'http://en.wikipedia.org/wiki/' + title
page = request.urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')
title = soup.find(id='firstHeading').contents[0]
print(title)

body = soup.find(id='bodyContent')
[x.extract() for x in body.find_all(['sup', 'span'])]
[x.extract() for x in body.find_all(role=['note', 'navigation'])]

wikiLinks = []

paragraphs = body.find_all('p')
for paragraph in paragraphs:
    links = paragraph.find_all('a')

    for link in links:
        link_string = link['href']
        wikiLinks.append(link)

[print(x) for x in wikiLinks]
