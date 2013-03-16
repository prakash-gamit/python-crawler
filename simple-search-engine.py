#!/usr/bin/env python

# Prakash Gamit <prakashgamit23@gmail.com>
# Indian Institute of Technology, Roorkee

import httplib


def getPage(host, protocol, url):
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


def printLinks(page):
    # print all the links on the @page

    while True:
        link, endpos = getNextLink(page)

        if link:
            # print only if its not the same page
            if link.find('#') == -1:
                print link

            page = page[endpos:]
        else:
            break

    return
# end printLinks()


def main():
    printLinks(getPage('localhost', 'HTTP', '/index.html'))
# end main()


if __name__ == '__main__':
    main()
