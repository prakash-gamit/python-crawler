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


def printLinks(page):
    # print all the links on the @page
    start_link = page.find('<a href=')

    while not (start_link == -1):
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        link = page[(start_quote + 1) : end_quote]

        # print only if its not the same page
        if link.find('#') == -1:
            print link

        start_link = page.find('<a href=', end_quote)
# end printLinks()

def main():
# end main()


if __name__ == '__main__':
    main()
