import httplib
import lxml.html


pid = 'b00ptsjd'
host = 'www.bbc.co.uk'
urlpath = '/programmes/%s/episodes/player' % pid
url = 'http://' + host + urlpath

print "Connecting to", host
conn = httplib.HTTPConnection(host)
print "Requesting", urlpath
conn.request("GET", urlpath)
res = conn.getresponse()
if res.status != 200:
    print "Error retrieving %s:" % url, res.status, res.reason

data = res.read()

print "Received", len(data), "bytes"

root = lxml.html.document_fromstring(data)

for div in root.findall('.//div/ol/li/div'):
    span = div.findall('.//div/h4/a/span/span')[0]
    prog_pid = div.get('data-pid')
    prog_url = div.get('resource')
    prog_name = span.text
    print prog_pid, prog_url, prog_name
