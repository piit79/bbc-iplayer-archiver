import lxml.html
import urllib2

URL_BASE = 'http://www.iplayerconverter.co.uk'
CONVERT = "/convert.aspx?pid={0:s}"
INFO = "/pid/{0:s}/default.aspx"


def get_rtmpdump_cmd(pid):
    """
    Return rtmpdump command line to download the specified iPlayer episode.
    :param pid: string
    :rtype: string
    """
    url = URL_BASE + CONVERT.format(pid)
    root = lxml.html.parse(url)
    codes = root.findall('.//p/code')
    if len(codes) == 1:
        return codes[0].text
    elif len(codes) < 1:
        print "pid2rtmpdump: <p><code> not found!"
        return False
    else:
        print u"pid2rtmpdump: more than one <p><code> elements found: {0:d}" \
            .format(len(codes))
        return False


def get_pid_info(pid):
    """
    Return pid info: vpid, aac link, hls playlist, wma link
    :param pid: string
    :rtype: dict
    """
    url = URL_BASE + INFO.format(pid)
    try:
        fp = urllib2.urlopen(url)
    except urllib2.URLError as ex:
        print u"Couldn't get info for pid {0:s}: {0:s}".format(pid, ex)
        return {}
    info = {}
    for line in fp:
        if line[:4] == 'pid=':
            for el in line.split(','):
                ell = el.split('=')
                if len(ell) == 2:
                    info[ell[0]] = ell[1]
            break
    return info
