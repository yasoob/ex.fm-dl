import urllib2
import json
import sys
import logging
import argparse
import platform


class Ex_fm(object):

    # main class for the downloader
    def __init__(self, query=None, num=20):
        self.query = query
        if self.query == None:
            sys.exit("You entered a wrong query!")
        self.num = num
        logging.debug("Query == "+self.query)
        logging.debug("Num == "+str(self.num))
        self.main_func()

    def search(self, query, num):
        query = query.replace(" ", "%20")
        search_url = 'http://ex.fm/api/v3/song/search/%s?start=0&results=%s' % (query, str(num))
        logging.debug("Search url == "+search_url)
        try:
            html = urllib2.urlopen(search_url)
        except urllib2.HTTPError:
            try:
                html = urllib2.urlopen(search_url)
            except urllib2.HTTPError:
                logging.warning("An error occured while getting the results. Please try again")
                sys.exit()
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
                logging.info(str(count) + ".  " + result[count]['title'] + " -by- " + result[count]['artist'])
            else:
                logging.info(str(count) + ".  " + result[count]['title'])
            count += 1
        logging.debug("Result == "+str(len(result)))
        return result

    def convertSize(self, n, format='%(value).1f %(symbol)s', symbols='customary'):
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

    def download(self, fileurl, file_name):
        u = urllib2.urlopen(fileurl)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        logging.info("Downloading %s (%s)" % (file_name, self.convertSize(file_size)))

        file_size_dl = 0
        block_size = 8192

        while True:
            buffer = u.read(block_size)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%s [%3.2f%%]" % (self.convertSize(file_size_dl), file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            logging.debug("Status == "+str(status))
            sys.stdout.write("\r        %s" % status)
        f.close()

    def main_func(self):
        results = self.search(self.query, self.num)
        songId = raw_input('\nWhich song do you want to download ?   ')
        url = results[int(songId)]['url']
        logging.debug("Url == "+url)
        title = results[int(songId)]['title']
        logging.debug("Title == "+title)
        logging.info("Downloading the file...")
        self.download(url, title + ".mp3")
        logging.info("Download completed\n")


def main():
    try:
        parser = argparse.ArgumentParser(description="Ex.fm song downloader made by M.Yasoob <yasoob.khld@gmail.com>")
        parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        parser.add_argument("-n", "--number", help = "Specify the number of results to retrieve", default=20)
        parser.add_argument("query", help = "the name of the song or artist to search for")
        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(format = "%(message)s", level=logging.DEBUG)
        else:
            logging.basicConfig(format = "%(message)s", level=logging.INFO)
        logging.debug("Arguments == "+str(args))
        logging.debug("Platform == %s" %(platform.platform()))
        logging.debug("Python version == %s" %(platform.python_version()))
        logging.info("Ex.fm song downloader made by M.Yasoob <yasoob.khld@gmail.com>")
        Ex_fm(args.query, args.number)
    except KeyboardInterrupt:
        sys.exit("\nProgram was closed by the user\n")

if __name__ == '__main__':
    main()
