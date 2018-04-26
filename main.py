from flask import Flask
import re
import operator
import urllib.request
import zipfile
import os

log_name = 'old.log'

def crack1():
    regex = re.compile(r'\[.+\] (host=old-website.com)')

    old_site_lines = []

    statuses = {}

    log = open(log_name)

    for l in log:
        match = re.search(regex, l)
        if match:
            status = l.split('"')[2]
            status = status.split()[0]
            status = status.split('=')[1]
            if int(status) != 200:
                if statuses.get(status):
                    statuses[status] += 1
                else:
                    statuses[status] = 1
    print(statuses)
    first = max(statuses.items(),
     key=operator.itemgetter(1))[0]
    print('First part of password: ', first)
    return int(first)

def crack2():
    regex = re.compile(r'\[.+\] host=.+ remote_addr=8.8.8.8')

    gDNS_lines = []

    count = 0

    log = open(log_name)
    for l in log:
        match = re.search(regex, l)
        if match:
            count = count + 1

    print('Second part of password: ', count)
    return count

def crack3():
    request = urllib.request.Request('http://hint.macpaw.io')
    opener = urllib.request.build_opener()
    firstdatastream = opener.open(request)
    etag =  firstdatastream.headers.get('ETag')
    print(etag)
    third = etag[1:3]
    print('Third part of password: ', third)
    return int(third)

def unzip():
    password = str(crack1() + crack2() + crack3())
    print('password is ', password)
    with zipfile.ZipFile('/tmp/additional.zip') as zip:
        zip.extractall('./', pwd=password.encode('ascii'))

def get_public_ip():
    with urllib.request.urlopen('http://ipinfo.io/ip') as response:
        return response.read().decode('utf-8')

unzip()
app = Flask(__name__)

@app.route('/')
def index():
    filez = os.listdir('tmp')
    file_name = filez[0]
    return '''My github profile is <b>github.com/revan730</b><br/>
    I'm a third year student at Kiev Polytechnic Institute,
    faculty of information and computer technologies, software engineering.<br/>
    I love solving puzzles, which is why i embeded a little script that cracks
    the password and unzips the file.
    The password for additional tasks is cracked,
     zip file is uncompressed, enjoy).<br/>
    Name of uncompressed file: ''' + file_name

@app.route('/ip')
def ip():
    return "Host's public ip address is <b>" + get_public_ip() + "</b>"



