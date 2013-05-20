#!/usr/bin/env python

# Prakash Gamit <prakashgamit23@gmail.com>
# Indian Institute of Technology, Roorkee

import urllib2
import argparse
import logging

# to use in getPageRank()
pageRanks = {}


def getPage(url):
    """
    get webpage @url from the Internet

    @args
    url => url of webpage to retrieve

    @return => return contents of webpage if successful in retrieving @url
               else return None
    """

    logging.info("Requesting %s", url)
    request = urllib2.Request(url)

    try:
        response = urllib2.urlopen(request)
        page = response.read()
        logging.info("Received %s", url)
    except urllib2.URLError as e:
        logging.warning("Error Retrieving %s", url)
        logging.info("Reason: %s", e.reason)
        return

    return page
# end getPage()


# return first link on the @page
def getNextLink(page):
    """
    get next link from the page

    @args
    page => contents of webpage

    @return => tuple containing link and end quote of link
    """

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
    """
    get all the links on the page

    @args
    page => contents of the webpage

    @return => list of all the links on the @page
    """

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
    """
    take union of two lists

    @args
    list1 => first list
    list2 => second list

    store the union of two lists in @list1

    @return => None
    """

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
        logging.info("Crawling %s", page)
        if page not in crawled:
            content = getPage(page)

            if content != None:
                logging.debug("Adding %s to index", page)
                addPageToIndex(index, page, content)
                logging.debug("Added %s to index", page)

                logging.debug("Getting all links from page %s", page)
                outlinks = getLinks(content)
                logging.debug("Got all links from page %s", page)
                graph[page] = outlinks

                union(tocrawl,outlinks)

            crawled.append(page)

    return index, graph
# end crawlWeb()


# add a @keyword and @url to our @index
def addToIndex(index, keyword, url):
    """
    add a @keyword and @url to @index
    """

    logging.debug("Adding (%s, %s) to index", keyword, url)
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
# end addToIndex()


# @lookup a keyword in @index and list of urls that contain that word
def lookup(index, keyword):
    """
    retrieve urls whose content contain @keyword from @index
    """

    logging.debug("Searching %s in index", keyword)
    if keyword in index:
        return index[keyword]
    return []
# end lookup()


# add words in @content to @index
def addPageToIndex(index, url, content):
    """
    add all the words in page to @index
    """

    words = content.split()
    for word in words:
        addToIndex(index, word, url)
# end addPageToIndex()


def computeRanks(graph):
    """
    compute page ranks of the urls
    """

    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)

    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
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


# return @pageRank of @url
def getPageRank(url):
    """
    return page rank of @url
    """

    global pageRanks
    return pageRanks[url]


# return pages in sorted order of their ranks
def lookupBest(index, keyword):
    """
    return list of urls that contain @keyword sorted according to their
        page ranks
    """

    if keyword in index:
        return sorted(index[keyword], key=getPageRank)

    return []
# end lookupBest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('seed', help='seed page for starting crawling')
    parser.add_argument('-v', '--verbose', action = 'count', default = 0,
                        help = 'increase verbosity of output')
    args = parser.parse_args()

    # set loglevel based on command line options
    if args.verbose == 2:
        loglevel = logging.DEBUG
    elif args.verbose == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    # configure logging
    logging.basicConfig(format="%(levelname)s:%(message)s", level=loglevel)

    seedPage = args.seed
    logging.info("Seed page = %s", seedPage)

    logging.info("Starting crawling...")
    index, graph = crawlWeb(seedPage)
    logging.info("Finished crawling...")

    logging.info("Computing Page Ranks")
    ranks = computeRanks(graph)
    logging.info("Computed Page Ranks")

    global pageRanks
    pageRanks = ranks

    print lookupBest(index, 'Nickel')
# end main()


if __name__ == '__main__':
    main()
