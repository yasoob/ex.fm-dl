import urllib2
import json
import sys


def search(query, num):
    query = query.replace(" ", "%20")
    search_url = 'http://ex.fm/api/v3/song/search/%s?start=0&results=%s' % (query, str(num))
    html = urllib2.urlopen(search_url)
    songs = html.read()
    songs = json.loads(songs)
    result = {}
    count = 1
    for i in songs['songs']:
        result[count] = {}
        result[count]['title'] = i['title']
        result[count]['artist'] = i['artist']
        result[count]['thumbnail'] = i['image']['large']
        result[count]['url'] = i['url']
        if result[count]['artist']:
            print str(count) + ".  " + result[count]['title'] + " -by- " + result[count]['artist']
        else:
            print str(count) + ".  " + result[count]['title']
        count += 1
    return result


def convertSize(n, format='%(value).1f %(symbol)s', symbols='customary'):
    """
    Convert n bytes into a human readable string based on format.
    symbols can be either "customary", "customary_ext", "iec" or "iec_ext",
    see: http://goo.gl/kTQMs
    """
    SYMBOLS = {
        'customary': ('B', 'K', 'Mb', 'G', 'T', 'P', 'E', 'Z', 'Y'),
        'customary_ext': ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                          'zetta', 'iotta'),
        'iec': ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
        'iec_ext': ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                    'zebi', 'yobi'),
    }
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)


def download(fileurl, file_name):
    u = urllib2.urlopen(fileurl)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading %s (%s)" % (file_name, convertSize(file_size))

    file_size_dl = 0
    block_size = 8192

    while True:
        buffer = u.read(block_size)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%s [%3.2f%%]" % (convertSize(file_size_dl), file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        #print status
        sys.stdout.write("\r        %s" % status)
        sys.stdout.flush()

    f.close()


if __name__ == '__main__':
    try:
        print "Ex.fm song downloader made by M.Yasoob <yasoob.khld@gmail.com>"
        query = raw_input("Which song or artist do you want to search for?   ")
        num = raw_input("How many results do you want to retrieve ?   ")
        print ""
        results = search(query, num)
        songId = raw_input('\nWhich song do you want to download ?   ')
        url = results[int(songId)]['url']
        title = results[int(songId)]['title']
        music = urllib2.urlopen(url)
        print "Downloading the file..."
        download(url, title + ".mp3")
    except KeyboardInterrupt:
        print "\nProgram was closed by the user\n"
        sys.exit()
