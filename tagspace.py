#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import wikipedia
import re
import sys

class ExtractLink:
    def __init__(self, article_html):
        self.soup = BeautifulSoup(article_html, "html.parser")
        self.soup = self.soup.find(id="mw-content-text")

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

    def is_valid_tag(self, tag):
        return tag.name == 'p' or tag.name == 'ul'

    def get_paragraphs(self):
        self.paragraphs = self.soup.find_all(self.is_valid_tag, recursive=False)

        return self.paragraphs

    def iterate_links(self):
        for each_paragraph in self.paragraphs:
            for each_link in each_paragraph.find_all("a"):
                href = each_link.get("href")
                if self.is_valid_link(str(href), str(each_paragraph)):
                    return each_link

        return False

    def get_first_link(self):
        self.get_paragraphs()
        first_link = self.iterate_links()

        return {"next_link": first_link.get('href'),
                "next_title": first_link.get('title'),
                "text": first_link.get('text')}

class IterateArticles:
    def __init__(self, start_page):
        self.start_page = start_page
        self.base_url = "http://en.wikipedia.org/w/index.php?title="

    def get_page(self, address):
        req = urllib2.Request(address)
        data = urllib2.urlopen(req).read()
        return data

    def traverse(self):
        page_name = self.start_page
        page_url = self.base_url + page_name + "&printable=yes"
        results = []

        while True:
            print page_name
            results.append(page_name)

            article_html = self.get_page(page_url)
            next_link_obj = ExtractLink(article_html).get_first_link()

            page_name = next_link_obj['next_link'][6:]
            page_url = self.base_url + page_name + "&printable=yes"            

            if page_name == 'Philosophy':
                print 'Philosophy'
                results.append('Philosophy')
                return results

if __name__ == "__main__":
    if len(sys.argv) > 0:
        try:
            results = IterateArticles(sys.argv[1])
            print results.traverse()
        except IndexError:
            print 'Format: python tagspace.py <page name>'
    else:
        print 'Format: python tagspace.py <page name>'

