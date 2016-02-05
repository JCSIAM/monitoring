'''
Created on Jan 27, 2016

@author: souvik
'''

import logging
from logging.handlers import TimedRotatingFileHandler
from abc import ABCMeta, staticmethod
from AbstractMetrics import AbstractMetrics, AbstractMetricsFactory 
import threading

threadLocal = threading.local()

class LogRotationFrequency:
    __metaclass__ = ABCMeta
    ''''This prevents instantiation of the class since it is an interface. This
    class however cannot be instantiated as it is an abstract class
    '''
        
    SECONDS = 's'
    MINUTE = 'm'
    HOUR = 'h'
    DAY = 'd'
        
class ThreadLocalMetrics(AbstractMetrics):
    __BACKUP_COUNT = 100
    ''' Number of files to retain in the log folder
    '''
    
    ''' TODO: Need to implement the actual thread local part. Right now i am coming up with the basic version so that clients can start using it
    '''
        
    def __init__(self, path, frequency, interval):
        '''
        Constructor
        '''
        super(ThreadLocalMetrics, self).__init__()
        self._initialize_metrics(path, frequency, interval=1);
        self.id = "xxxx"
        threadLocal.metrics = self;
    
    @staticmethod
    def get():
        return threadLocal.metrics
    
    def _initialize_metrics(self, path, frequency, interval):
        self.__create_timed_rotating_log(path, frequency, interval)    
        
    def _flush_metrics(self):
        ''' This just prints out the Metric object 
        '''
        self.__logger.info(self.__str__());
        
    def __getitem__(self, k):
        if k == 'id':
            return self.id
        else:
        #    return super.__getattribute__()
            return None
        
    def __create_timed_rotating_log(self, path, frequency, interval):
        ''' This method describes the logging type of service logs
        '''
        # TODO: rotate to gzip format
        self.__logger = logging.getLogger("service.log")
        self.__logger.setLevel(logging.INFO)
        handler = TimedRotatingFileHandler(path, frequency, interval, ThreadLocalMetrics.__BACKUP_COUNT)
        self.__logger.addHandler(handler)
            
    def __str(self):
        return super().__str__()
    
    
           
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
        
    def with_log_rotation_frequency_and_interval(self, frequency, interval=1):
        self.__frequency = frequency
        self.__interval = interval
        return self
        
    def create_metrics(self):
        
        metrics = ThreadLocalMetrics(self.__service_log_path, self.__frequency, self.__interval)
        self._add_metric_attributes(metrics)
        return metrics   


