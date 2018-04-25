import urllib2
import urllib
import time
import socket
import os,sys
import shutil
import gevent
from gevent.threadpool import ThreadPool
from gevent.queue import JoinableQueue
from gevent.queue import Empty
from gevent import monkey
monkey.patch_all()

#pid = os.getpid()
#os.system('sh monitor.down.script.sh %s &' %pid)

#
def callbackfunc(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "** downloading : %.2f%% -- %s **" % (percent,id)
#
def download(id) :
    url = 'https://api.gdc.cancer.gov/data/%s' % id
    filename = dic[id][0]
    filepath = dic[id][1]
    abs_path = os.path.join(filepath,filename)
    if os.path.exists(abs_path) :
        print '*** file %s existed ***' % ( filename + ' '*(60-len(filename)))
        pass
    else :
        num =1
        while num <=5 :
	    try :
		tim = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print '* start %s downloading * cycle %s ! time is : %s ! *' % (id,num,tim)
		#gevent.sleep(0.2)
		#print id 
		socket.setdefaulttimeout(3500)
                urllib.urlretrieve(url,'./tmp/%s'% id)
                print '* %s has downloaded *' % id
                shutil.move('./tmp/%s' %id,abs_path)
                break
            except Exception,er :
                print er,'* try again ! *'
                num += 1
                pass
	if num > 5 :
	    print 'download failed ! '
#
def working():
    while True:
        id = q.get()
        download(id)
        q.task_done()

#################
# start working #
#################
cwd = os.getcwd()
q = JoinableQueue()
file = open(sys.argv[1],'r')
dic = {}

for line in file :
    line = line.split('\t')
    name = line[2]
    project = line[7]
    id = line[8]
    cate = line[9]
    case = line[11]
    q.put(id)
    path = '%s/Date_Pool_All_Files/%s/%s' % (cwd,project,case)
    if not os.path.exists(path) : 
        os.makedirs(path)
    dic[id] = (name,path)

jobs = [gevent.spawn(working) for i in xrange(50)]
q.join()

print 'All files has downloaded ! ~\(^v^)/~ Go for a rest ! ~\(^v^)/~'
