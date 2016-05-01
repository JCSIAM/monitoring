'''
Created on Jan 27, 2016

@author: souvik


################## This is just a test class for demonstration purpose only. Remove this class ASAP #############################
'''
import logging

from metrics.NullMetrics import NullMetricsFactory
from metrics.ThreadLocalMetrics import ThreadLocalMetricsFactory
from metrics.Metrics import Metrics, Unit
from datetime import datetime
from time import time, sleep

#from time import time
#from socket import socket
import threading
import time

exitFlag = 0

def print_logs(name):

        i = 0
        while i<10:
            metricsFactory = ThreadLocalMetricsFactory("/var/log/cinder/service_log")
            print metricsFactory
            metrics =  metricsFactory.create_metrics()
            metrics.add_property("RequestId", "q311-r329-r302-jf2j-f92f-if93-"+name)
            metrics.add_property("Id", str(i))
            metrics.add_date("Sample_Date_Field",  time.time())
            metrics.add_count("Success", 1)
            metrics.add_count("Failure", 0)
            metrics.add_count("Error", 0)
            metrics.add_count("Fault", 0)
            metrics.add_count("Retry", 0)
            metrics.add_time("DatebaseConnectionTime", 500, Unit.MILLIS)
            metrics.add_time("RetryWaitTime", 1, Unit.SECONDS)

            sleep(0.1)
            metrics.close()

            i = i+1
            print i

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.__metricsFactory = ThreadLocalMetricsFactory("/tmp/service_log").with_account_id("xxxxxxxxxxxxxxx").with_marketplace_id("IDC1").with_program_name("CinderAPI").with_operation_name("CreateVolume")

    def run(self):
        print "Stating"
        print_logs( self.name)
        print "Exiting " + self.name




def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1


if __name__ == '__main__':
    logging.basicConfig(filename="/var/log/cinder/cinder-api.log", level=logging.DEBUG)

    #thread1 = myThread(1, "Thread-1", 1)
    #thread2 = myThread(2, "Thread-2", 2)

    # Start new Threads
    #thread1.start()
    #thread2.start()
    print_logs("Main")


print "Exiting Main Thread"

'''
Test using this
import os
os.rename('my.log', 'my.log-old')
logging.info('Hello, New World!')

'''