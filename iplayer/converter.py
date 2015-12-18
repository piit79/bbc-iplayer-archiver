import lxml.html

URL_BASE = 'http://www.iplayerconverter.co.uk'
CONVERT = '/convert.aspx?pid=%s'


def pid2rtmpdump(pid):
    """
    Return rtmpdump command line to download the specified iPlayer episode.
    :param pid: string
    :rtype: string
    """
    url = URL_BASE + CONVERT % pid
    root = lxml.html.parse(url)
    codes = root.findall('.//p/code')
    if len(codes) == 1:
        return codes[0].text
    elif len(codes) < 1:
        print 'pid2rtmpdump: <p><code> not found!'
        return False
    else:
        print 'pid2rtmpdump: more than one <p><code> elements found: %d' % \
              len(codes)
        return False
