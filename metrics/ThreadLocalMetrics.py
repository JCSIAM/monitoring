'''
Created on Jan 27, 2016

@author: souvik
'''

import logging
from logging.handlers import TimedRotatingFileHandler
from abc import ABCMeta
from AbstractMetrics import AbstractMetrics, AbstractMetricsFactory
import threading

def create_timed_rotating_log(path):
    ''' This method describes the logging type of service logs
    '''
    logger = logging.getLogger("service.log")
    # logger.propagate = False
    # Uncomment this after thorough validation in Production, that all metrics are in service
    # logs. This will remove the service logs from cinder API.
    handler = logging.handlers.WatchedFileHandler(path)
    # Cinder itself uses watched file handler. LogRotation is handled externally using logrotate.d
    logger.addHandler(handler)
    return logger

# TODO: This needs to be configurable and passed through in the class.
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

    def _initialize_metrics(self):
        pass

    def _flush_metrics(self):
        ''' This just prints out the Metric object
        '''
        logger.info(self.__str__())

    def __str(self):
        return super(self).__str__()

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

    def create_metrics(self):

        metrics = ThreadLocalMetrics()
        self._add_metric_attributes(metrics)
        return metrics
