# ex01_scraping.py


from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, "html.parser")
print(soup.prettify())

print()

print(soup.title)

print()

print(soup.p)  # 가장 처음에 있는 p 태그를 가져온다.

print()

print(soup.find("p", "story"))  # 첫 번째 인자는 태그, 두 번째 인자는 클래스를 입력하면 된다.

print()

print(soup.find("p", "story").text)
