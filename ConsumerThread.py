import threading
import time
import logging
import random
import Queue
from nbstreamreader import NonBlockingStreamReader as NBSR

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

BUF_SIZE = 10
q = Queue.Queue(BUF_SIZE)

class Stream(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(Stream,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        nbsr = NBSR(open("streamingdata/datgen2-test.data"))
        while True:
            if not q.full():
                output = nbsr.readline(0.1)
                if not output:
                    print '[No more data]'
                    break
                #item = random.randint(1,10)
                q.put(output)
                logging.debug('Putting ' + str(output)  
                              + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(random.random())    
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                logging.debug('Getting ' + str(item) 
                              + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(random.random())
        return

if __name__ == '__main__':
    
    stream = Stream(name='stream')
    c = ConsumerThread(name='consumer')

    stream.start()
    time.sleep(2)
    c.start()
    time.sleep(2)