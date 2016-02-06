'''
Created on Jan 27, 2016

@author: souvik
'''

import logging
from logging.handlers import TimedRotatingFileHandler
from abc import ABCMeta
from AbstractMetrics import AbstractMetrics, AbstractMetricsFactory 
import threading

#threadLocal = threading.local()
__BACKUP_COUNT = 100

class LogRotationFrequency:
    __metaclass__ = ABCMeta
    ''''This prevents instantiation of the class since it is an interface. This
    class however cannot be instantiated as it is an abstract class
    '''
        
    SECONDS = 's'
    MINUTE = 'm'
    HOUR = 'h'
    DAY = 'd'

def create_timed_rotating_log(path, frequency = LogRotationFrequency.HOUR, interval = 1):
    ''' This method describes the logging type of service logs
    '''
    # TODO: rotate to gzip format
    #logger = logging.getLogger("service.log")
    #logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(path, frequency, interval, __BACKUP_COUNT)
    logger.addHandler(handler)
    return logger;
        
logger = create_timed_rotating_log("/var/log/cinder/service.log")

        
class ThreadLocalMetrics(AbstractMetrics):
    ''' Number of files to retain in the log folder
    '''
    
    __threadLocal = threading.local()
        
    def __init__(self):
        '''
        Constructor
        '''
        super(ThreadLocalMetrics, self).__init__()
        ThreadLocalMetrics.__threadLocal.metrics = self
    
    @staticmethod
    def get():
        return ThreadLocalMetrics.__threadLocal.metrics
    
    def _initialize_metrics(self, path, frequency, interval):
        pass
 
    def _flush_metrics(self):
        ''' This just prints out the Metric object 
        '''
        logger.info(self.__str__());
        
    def __str(self):
        return super().__str__()
    
    def close(self):
        super(ThreadLocalMetrics, self).close()
        ThreadLocalMetrics.__threadLocal.__dict__.clear()
        
           
class ThreadLocalMetricsFactory(AbstractMetricsFactory):
    ''' Factory method to create Thread Local Metrics
    Example Usage:
    metricsFactory = ThreadLocalMetricsFactory("/tmp/service_log").with_account_id("xxxxxxxxxxxxxxx").with_marketplace_id("IDC1").with_program_name("CinderAPI").with_operation_name("CreateVolume");
    metrics =  metricsFactory.create_metrics();
    '''
    
    def __init__(self, service_log_path):
        super(ThreadLocalMetricsFactory, self).__init__()
        self.__service_log_path = service_log_path
        self.__interval = 1
        self.__frequency = LogRotationFrequency.HOUR
        
        
    def create_metrics(self):
        
        metrics = ThreadLocalMetrics()
        self._add_metric_attributes(metrics)
        return metrics
   
