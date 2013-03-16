#!/usr/bin/env python

# Prakash Gamit <prakashgamit23@gmail.com>
# Indian Institute of Technology, Roorkee

import httplib


def getPage(host, url, protocol = 'HTTP'):
    if protocol == 'HTTP':
        conn = httplib.HTTPConnection(host)
    else:
        conn = httplib.HTTPSConnection(host)

    conn.request('GET', url)
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
    for item in list1:
        if item not in list2:
            list1.append(item)
# end union


def main():
    links = getLinks(getPage('localhost', '/index.html'))
    print links
# end main()


if __name__ == '__main__':
    main()
