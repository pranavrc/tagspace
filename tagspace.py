#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import re

class ExtractLink:
    def __init__(self, article_html):
        self.soup = BeautifulSoup(article_html, "html.parser")
        self.cleaned_paragraph = None

    def clean_parantheses(self, content):
        return re.sub(r'\([^)]*\)', '', content)

    def is_valid_link(self, href, paragraph):
        if not href or "#" in href or "//" in href or ":" in href:
            return False
        if "/wiki/" not in href:
            return False
        if href not in paragraph:
            return False
        
        prefix = paragraph.split(href, 1)[0]

        if prefix.count("(") != prefix.count(")"):
            return False

        return True

    def get_first_paragraph(self):
        self.cleaned_paragraph = self.soup.find_all('p')[0]

        return self.cleaned_paragraph

    def iterate_links(self):
        for each_link in self.cleaned_paragraph.find_all("a"):
            href = each_link.get("href")
            if self.is_valid_link(str(href), str(self.cleaned_paragraph)):
                return each_link

        return False

    def get_first_link(self):
        self.get_first_paragraph()
        first_link = self.iterate_links()

        return {"next_link": first_link.get('href'),
                "next_title": first_link.get('title'),
                "text": first_link.get('text')}

class IterateArticles:
    def __init__(self, start_page):
        self.start_page = start_page
        self.start_url = "http://en.wikipedia.org/w/index.php?title=" + start_page + "&printable=yes"

    def get_page(self, address):
        req = urllib2.Request(address, headers={'User-Agent' : "Magic Browser"})
        return urllib2.urlopen(req).read()

    def traverse(self):
        page_name = self.start_page
        results = []

        while True:
            print page_name
            results.append(page_name)

            article_html = self.get_page(self.start_url)
            next_link_obj = ExtractLink(article_html).get_first_link()

            page_name = next_link_obj['next_title']

            if page_name == 'Philosophy':
                return results
