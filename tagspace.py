#!/usr/bin/env python

'''
https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy

Script that prints the titles of every article from a start
article on the way to Philosophy.
'''

from bs4 import BeautifulSoup
import urllib2
import wikipedia
import re
import sys

class ExtractLink:
    ''' Class containing subroutines to parse html
    and return the first valid link in a Wikipedia article.'''
    def __init__(self, article_html):
        self.soup = BeautifulSoup(article_html, "html.parser")
        self.soup = self.soup.find(id="mw-content-text")

    def clean_parentheses(self, content):
        ''' Remove content inside parentheses. '''
        return re.sub(r'\([^)]*\)', '', content)

    def is_valid_link(self, href, paragraph):
        ''' A link is valid only if:
            1. It is not an external link or an anchor or a Help link.
            2. It is not within parentheses.
        '''
        if not href or "#" in href or "//" in href or ":" in href \
        or "/wiki/" not in href or href not in paragraph:
            return False

        prefix = paragraph.split(href, 1)[0]

        if prefix.count("(") != prefix.count(")"):
            return False

        return True

    def is_valid_tag(self, tag):
        ''' The only valid tags are <p> and <ul> tags. '''
        return tag.name == 'p' or tag.name == 'ul'

    def get_paragraphs(self):
        ''' Get all valid, top-level paragraphs from the article. '''
        self.paragraphs = self.soup.find_all(self.is_valid_tag, recursive=False)

        return self.paragraphs

    def iterate_links(self):
        ''' Iterate through all links in each paragraph
            and output the first valid link encountered. '''
        for each_paragraph in self.paragraphs:
            for each_link in each_paragraph.find_all("a"):
                href = each_link.get("href")
                if self.is_valid_link(str(href), str(each_paragraph)):
                    return each_link

        return False

    def get_first_link(self):
        ''' Wrapper function to run other subroutines and
            output a dictionary of info about the next article. '''
        self.get_paragraphs()
        first_link = self.iterate_links()

        return {"next_link": first_link.get('href'),
                "next_title": first_link.get('title'),
                "text": first_link.get('text')}

class IterateArticles:
    ''' Class with subroutines to traverse the first links from
    the start article to Philosophy. '''
    def __init__(self, start_page):
        self.start_page = start_page
        self.base_url = "http://en.wikipedia.org/w/index.php?title="

    def get_page(self, address):
        ''' Fetch html of the page from address. '''
        req = urllib2.Request(address)
        data = urllib2.urlopen(req).read()
        return data

    def traverse(self):
        ''' Traverse the first links from the start article,
        recursively until Philosophy is reached. '''
        page_name = self.start_page
        page_url = self.base_url + page_name + "&printable=yes"
        results = []

        while True:
            sys.stdout.write(page_name + ' -> ')
            sys.stdout.flush()

            results.append(page_name)

            article_html = self.get_page(page_url)
            next_link_obj = ExtractLink(article_html).get_first_link()

            page_name = next_link_obj['next_link'][6:]
            page_url = self.base_url + page_name + "&printable=yes"

            if page_name == 'Philosophy':
                print 'Philosophy'
                results.append('Philosophy')
                return results
            elif page_name in results:
                print 'Loop detected.'
                return results

if __name__ == "__main__":
    if len(sys.argv) > 0:
        try:
            results = IterateArticles(sys.argv[1])
            results.traverse()
        except IndexError:
            print 'Format: python tagspace.py <page name>'
    else:
        print 'Format: python tagspace.py <page name>'

