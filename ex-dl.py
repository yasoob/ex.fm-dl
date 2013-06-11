import urllib2
import json
import sys
import subprocess
import os

entry = """This program uses wget for downloading the song so right now it
is available only for linux and mac and not for windows. However 
I am working on making a windows version as well. :)\n"""

def search(query, num):
	query = query.replace(" ","%20")
	search_url = 'http://ex.fm/api/v3/song/search/%s?start=0&results=%s' %(query , str(num))
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
	    if result[count]['artist'] :
	    	print str(count) + ".  " + result[count]['title'] + " -by- " + result[count]['artist']
	    else:
	    	print str(count) + ".  " + result[count]['title'] 
	    count += 1
	return result

if __name__ == '__main__':
	try:
		print "Ex.fm song downloader made by M.Yasoob <yasoob.khld@gmail.com>"
		print entry
		query = raw_input("Which song or artist do you want to search for?   ")
		num = raw_input("How many results do you want to retrieve ?   ")
		print ""
		results = search(query,num)
		songId = raw_input('\nWhich song so you want to download ?   ')
		url = results[int(songId)]['url']
		title = results[int(songId)]['title']
		music = urllib2.urlopen(url)
		print "Downloading the file..."
		cmd = 'wget -O "%s.mp3" "%s"' % ( title, url) #Run wget to download the song
		p = subprocess.Popen(cmd, shell=True)
	except KeyboardInterrupt:
		print "\nProgram was closed by the user\n"
		sys.exit()