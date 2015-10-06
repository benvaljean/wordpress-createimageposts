#wordpress-createimageposts

#(c) Benjamin Goodacre 2015

import ConfigParser
import os, itertools, datetime, time, sys, getopt
from PIL import Image
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

version = "1.9.12"

def showhelp():
	print sys.argv[0] + " v" + version
	print "Usage: " + sys.argv[0] + " --site=[all|site-name] --title=[all|dir-name] --date=[all|inc] --version"
def updatesite(site):
	titlelistdir = {}
	wp = Client(config.get(site, 'WPxmlrpcUrl'), config.get(site, 'WPUser'), config.get(site, 'WPPass'))
	for o,p in opts:
		if o in ['-t','--title']:
			if p != 'all':
				#just 1 dir, add only the given dir to the dict
				titlelistdir[p.strip()] = p.lower().replace(' ','-').strip()
	if not titlelistdir:
		#all dirs
		print 'all titles set'
		titlelist = open(config.get(site, 'TitlesList'),'r')
		for line in titlelist.readlines():
			titlelistdir[line.strip()] = line.lower().replace(' ','-').strip()
	for title in titlelistdir:
		dir = config.get(site, 'MediaRoot') + titlelistdir[title]
		mtime = lambda f : datetime.datetime.fromtimestamp(os.path.getmtime(dir + '/' + f))
		print title + ' ' + dir
		#tuple 4=by the hour  3=by the day
		mtime_hour = lambda f: datetime.datetime(*mtime(f).timetuple()[:4])
		dir_files = sorted(os.listdir(dir), key=mtime)
		dir_files = filter(lambda f: '150x150' not in f and '_p.jpg' not in f and f.lower().endswith(('.jpg','.jpeg','.png','.gif')) , dir_files)
		if doallpics == 0:
			dir_files = filter(lambda f: datetime.datetime.strptime(lastrun,'%Y-%m-%d %H:%M:%S') < mtime(f), dir_files)
		#dir_files = filter(lambda f: datetime.datetime(2010,1,1,0) <	mtime(f) < datetime.datetime(2015,1,1,0), dir_files)
		by_hour = dict((k,list(v)) for k,v in itertools.groupby(dir_files, key=mtime_hour)) #python 2.6
		print by_hour
		for f in by_hour:
			print f
			post = WordPressPost()
			post.title = title
			post.terms_names = {
			'post_tag': [title],
			'category': []
			}
			tagsfilename = dir + '/_tags.txt'
			catsfilename = dir + '/_cats.txt'
	
			if os.path.isfile(tagsfilename):
				taglist = open(tagsfilename,'r')
				print tagsfilename
				for l in taglist.readlines():
					post.terms_names['post_tag'].append(l.strip())
			if os.path.isfile(catsfilename):
				catlist = open(catsfilename,'r')
				for li in catlist.readlines():
					post.terms_names['category'].append(li.strip())
			print post.terms_names
			post.content = ''
			for pic in by_hour[f]:
	#		   if pic.lower().endswith(('.jpg','.jpeg','.png','.gif')):
	#			   if '150x150' not in pic:
						urlroot = config.get(site, 'MediaRootURL') 
						fileName, fileExtension = os.path.splitext(pic)
						try:
							im = Image.open(dir + '/' + pic)
							(width, height) = im.size
						except:
							width = ''
							height =''
							pass
						entry='<a href="' + urlroot + titlelistdir[title] + '/' + pic + '"><img class="alignnone size-medium tooltips" title="' + str(width) + ' x ' + str(height) + '" src="' + urlroot + titlelistdir[title] + '/' + fileName + '-150x150' + fileExtension + '"></a>'
						#print entry
						post.content += entry
	
			post.content = post.content.strip()
			print post.content
			pattern = '%Y-%m-%d %H:%M:%S'
	#	   epoch = int(time.mktime(time.strptime(f, pattern)))
	
	#	   date_time = '03-03-2015 23:28:48'
	#	   pattern = '%d-%m-%Y %H:%M:%S'
	#	   epoch = int(time.mktime(time.strptime(date_time, pattern)))
	
	
			post.date = f
			post.post_status = 'publish'
			wp.call(NewPost(post))
	
	if doallpics == 0:
		print 'Newpost appears added OK, updating lastrun'
		with open (lastrunfile, "w") as myfile:
			myfile.write(time.strftime("%Y-%m-%d %H:%M:%S"))
	

try:
	opts,remainder = getopt.getopt(sys.argv[1:],'t:vs:d:h',['title=','version','site=','date=','help'])
except getopt.GetoptError as err:
	print str(err)
	showhelp()

scriptdir = os.path.dirname(os.path.abspath(sys.argv[0]))

configfile = scriptdir + '/createposts.cfg'
config = ConfigParser.ConfigParser()
config.read(configfile)

#Set defaults
site='all' #all sites
doallpics=0 #upload pics from last run only

if len(sys.argv) == 1:
	showhelp()
	sys.exit(1)
else:
	for o,p in opts:
		if o in ['-d','--date']:
			print 'we have date set'
			if p == 'all':
				doallpics = 1
			elif p == 'inc':
				doallpics = 0
			else:
				showhelp()
				print "Syntax error: --date takes argument 'all' or 'inc'"
				sys.exit(1)
		elif o in ['-s','--site']:
			if p == 'all':
				site='all'
			else:
				if p not in config.sections():
					print p + ' section not found in config file ' + configfile
					sys.exit(1)
				site=p
		elif o in ['-v','--version','--help']:
			showhelp()
			sys.exit(0)

print 'site is' + site

if doallpics == 0:
	#read from the lasttun file and set the var
	lastrunfile = scriptdir + '/' + sys.argv[0] + '.' + site + '.lastrun'
	if os.path.isfile(lastrunfile):
		with open (lastrunfile, "r") as myfile:
			lastrun=myfile.read().replace('\n', '')
		print "last run " + lastrun
	else:
		#section exists but not lastrun file - presume doallpics = 1
		d = raw_input('Lastrun file not found, continuing with all pics anyway? Press <Enter> to continue of Ctrl-C to exit')
		doallpics = 1
	
if site == 'all':
	for each_section in config.sections():
		print each_section
		print config.get(each_section, 'WP-User')
		updatesite(each_section)
else:
	updatesite(site)
