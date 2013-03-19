#!/usr/bin/env python

# Prakash Gamit <prakashgamit23@gmail.com>
# Indian Institute of Technology, Roorkee

import httplib


def getPage(url, protocol = 'http'):
    temp1 = url.find('://')
    temp2 = url.find('/', temp1 + 3)

    host = url[(temp1 + 3):temp2]
    resource = url[temp2:]

    if protocol == 'http':
        conn = httplib.HTTPConnection(host)
    else:
        conn = httplib.HTTPSConnection(host)

    conn.request('GET', resource)
    response = conn.getresponse()

    if response.status == 200:
        return response.read()

    return
# end getPage()


# return first link on the @page
def getNextLink(page):
    start_link = page.find('<a href=')

    # stopping condition
    if start_link == -1:
        return None, 0

    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    link = page[(start_quote + 1) : end_quote]

    return link, end_quote
# end getNextLink()


def getLinks(page):
    # print all the links on the @page
    links = []

    while True:
        link, endpos = getNextLink(page)

        if link:
            # print only if its not the same page
            if link.find('#') == -1:
                links.append(link)

            page = page[endpos:]
        else:
            break

    return links
# end getLinks()


# store union of @list1 and list2 in list1
def union(list1, list2):
    for item in list2:
        if item not in list1:
            list1.append(item)
# end union


def crawlWeb(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}

    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = getPage(page)

            addPageToIndex(index, page, content)

            outlinks = getLinks(content)
            graph[page] = outlinks

            union(tocrawl,outlinks)
            crawled.append(page)

    return index, graph
# end crawlWeb()


# add a @keyword and @url to our @index
def addToIndex(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
# end addToIndex()


# @lookup a keyword in @index and list of urls that contain that word
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    return []
# end lookup()


# add words in @content to @index
def addPageToIndex(index, url, content):
    words = content.split()
    for word in words:
        addToIndex(index, word, url)
# end addPageToIndex()


def computeRanks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)

    for page in graph:
        ranks[page] = 1.0 / npages

    for i in ranks(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages

            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank

        ranks = newranks

    return ranks
# end computeRanks()


def main():
    index, graph = crawlWeb('http://localhost/test.html')
    print index
    print graph

    print lookup(index, 'test')
# end main()


if __name__ == '__main__':
    main()
