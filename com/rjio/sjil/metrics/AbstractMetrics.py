'''
Created on Jan 27, 2016

@author: souvik
'''
from Metrics import Metrics, MetricsFactory, Unit
from abc import ABCMeta, abstractmethod
from time import time
from datetime import datetime
import socket
import os

class AbstractMetrics(Metrics):
    ''' This class implements some methods from the Metric Interface.
    '''
    __STARTLINE = "===================================================================\n"
    __EQUALS = "="
    __LINE_BREAK = "\n"
    __COMMA = ","
    __TIMING = "Timing"
    __COUNTERS = "Counters"
    __BLANK = " "
    __EOE = "EOE"

    __metaclass__ = ABCMeta
    '''This prevents instantiation of the class since it is an interface. This
    class however cannot be instantiated as it is an abstract class
    '''
    
    @abstractmethod    
    def _initialize_metrics(self):
        '''
        This perform all the tasks at the start of a metrics lifecycle
        '''
        pass

    def __init__(self):
        self.__block_mutates = True
        # TODO: Figure out whether initializations required
        self.__properties = {}
        self.__dates = {}
        self.__timing = {}
        self.__counters = {}
        self.__metrics = {}
        self.__display_string = []
        self.__start_time = time()
            
    def add_property(self, name, value):
        if (self.__block_mutates == True): 
            self.__properties[name] = value
        
    
    def add_date(self, name, value):
        if (self.__block_mutates == True): 
            self.__dates[name] = value
        
    def add_count(self, name, value):
        # TODO: think of possible normalizations
        if (self.__block_mutates == True): 
            self.__counters[name] = value

    def add_time(self, name, value, unit):
        if (self.__block_mutates == True): 
            normalizedValue = self.__normalizeTimeToMillis(value, unit) 
            self.__timing[name] = normalizedValue

    @abstractmethod    
    def _flush_metrics(self):
        '''
        This perform all the tasks at the end of a metrics lifecycle and flushes the metric to an output
        '''
        pass

    def close(self):
        self.__end_time = time()
        self.__time_in_millis = int((self.__end_time - self.__start_time)*1000)
        self.__block_mutates = True
        self._flush_metrics()
        
    
    def __str__(self):
        self.__display_string.append(AbstractMetrics.__STARTLINE)
        self.__append_item("StartTime", self.__start_time, None, AbstractMetrics.__LINE_BREAK)
        formatted_end_time =datetime.fromtimestamp(self.__end_time).strftime('%Y-%m-%d %H:%M:%S') 
        self.__append_item("EndTime", formatted_end_time, None, AbstractMetrics.__LINE_BREAK)
        self.__append_item("Time", self.__time_in_millis, "ms", AbstractMetrics.__LINE_BREAK)
        ''' Creating special print format from basic time data'''
        # TODO: Create more specialized metrics display
        
        self.__append_to_display_string(self.__properties.iteritems(), None, AbstractMetrics.__LINE_BREAK) 
        ''' display all the properties'''
        
        self.__append_to_display_string(self.__dates.iteritems(), None, AbstractMetrics.__LINE_BREAK)  
        ''' display all the date items'''
        
        self.__append_items_in_same_line(AbstractMetrics.__TIMING, self.__timing, Unit.MILLIS)
        ''' display all the timing items'''
        
        self.__append_items_in_same_line( AbstractMetrics.__COUNTERS, self.__counters, None)
        ''' display all the counters items'''
        
        self.__display_string.append(AbstractMetrics.__EOE)
        ''' display end of metrics'''
        return ''.join(self.__display_string)
    
    def __append_to_display_string(self, iterable, unit, delimiter):
        ''' Goes through a list of items and print all lists
        '''
        for key, value in iterable:
            self.__append_item(key, value, unit, delimiter)
            
    def __append_item(self, key, value, unit, delimiter):
        ''' Add a metrics record. For example,
            ProgramName=CinderAPI or DatabaseConnectionTime=500 ms,
        '''
        self.__display_string.append(key)
        self.__display_string.append(AbstractMetrics.__EQUALS)
        self.__display_string.append(value.__str__())
        if unit:
            self.__display_string.append(AbstractMetrics.__BLANK)
            self.__display_string.append(unit.__str__())
        self.__display_string.append(delimiter)
    
    def __append_items_in_same_line(self, header, items, unit):
        ''' This creates a output like this
         Timing=DatabaseConnectionTime=500 ms,RetryWaitTime=1000 ms,
         Counters=Failure=0,Fault=0,Retry=0,Success=1,Error=0,
        '''
        #TODO: Remove delimeter from the last item
        if (items > 0):
            self.__display_string.append(header)
            self.__display_string.append(AbstractMetrics.__EQUALS)
            self.__append_to_display_string(items.iteritems(), unit, AbstractMetrics.__COMMA)
            self.__display_string.append(AbstractMetrics.__LINE_BREAK)    
    
    def __normalizeTimeToMillis(self, value, unit):
        ''' Change all time units to Milliseconds'''
        if (unit == Unit.SECONDS):
            return value * 1000
        else:
            return value
        
    def __isTimingMetric(self, unit):
        return (unit == Unit.SECONDS or unit == Unit.MILLIS)

class AbstractMetricsFactory(MetricsFactory):
    ''' An abstract factory which creates some basic attributes of a metric object
    '''
    
    __metaclass__ = ABCMeta
    '''This prevents instantiation of the class since it is an interface. This
    class however cannot be instantiated as it is an abstract class
    '''
    
    def __init__(self):
        self._prognam_name = None    
        self._operation_name = None
        self._account_id = None
        self._marketplace_id = None
        self._request_id = None
        
    def with_program_name(self, prognam_name):    
        self._prognam_name = prognam_name
        return self
            
    def with_operation_name(self, operation_name):    
        self._operation_name = operation_name
        return self
        
    def with_account_id(self, account_id):    
        self._account_id = account_id
        return self
        
    def with_marketplace_id(self, marketplace_id):
        self._marketplace_id = marketplace_id
        return self
   
    def with_request_id(self, request_id):
        self._request_id = request_id
        return self
   
    def _add_metric_attributes(self, metrics):
        metrics.add_property("HostName", socket.gethostname())
        metrics.add_property("PID", os.getpid())
        
        if (self._prognam_name is not None):
            metrics.add_property("ProgramName", self._prognam_name)    
            
        if (self._operation_name is not None):
            metrics.add_property("OperationName", self._operation_name)
            
        if (self._account_id is not None):
            metrics.add_property("AccountId", self._account_id)
            
        if (self._marketplace_id is not None):
            metrics.add_property("MarketplaceId", self._marketplace_id)
        self._request_id = None 
        if (self._request_id is not None):
            metrics.add_property("RequestId", self._request_id)
        
        
    