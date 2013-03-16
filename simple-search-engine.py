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


def main():
# end main()


if __name__ == '__main__':
    main()
