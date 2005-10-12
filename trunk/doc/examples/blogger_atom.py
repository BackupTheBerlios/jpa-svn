import httplib
import binascii
import time

userName = "user"
password = "secret"
blogId = "1234567890"
path = "http://www.blogger.com/atom/%s" % blogId

created = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

cookie = binascii.b2a_base64("%s:%s" % (userName, password))
headers = {
    "Content-type": 'application/atom+xml',
    "Authorization": 'BASIC %s' % cookie.strip(),
    "UserAgent": 'pyatomblogger',
    }

body = """<?xml version="1.0" encoding="UTF-8" ?>
<entry xmlns="http://purl.org/atom/ns#">
<generator url="http://jpa.berlios.de/">JPA-1.0</generator>
<title mode="escaped" type="text/html">Hello world</title>
<issued>%s</issued>
<content type="application/xhtml+xml">
<div xmlns="http://www.w3.org/1999/xhtml">Testing the AtomAPI</div>
</content>
</entry>""" % created

conn = httplib.HTTPConnection('proxy_host:8081')
conn.set_debuglevel(1)
conn.request("POST", path, body, headers)
response = conn.getresponse()
print "Response:", response.read()
conn.close()