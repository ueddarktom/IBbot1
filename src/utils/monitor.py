import os 
import pandas as pd
from time import time, localtime, strftime
import psutil

def get_process_memory_usage():
    """
    Returns the memory usage of the current process in MB.
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

class GetFuncExecutionTime(object):
    """
    Decorator to measure the execution time of a function.
    """
    def __init__(self):
        
        time_log = pd.DataFrame(columns=['class', 'funtion', 'start_time', 'end_time', 'execution_time', 'memory_usage'])
        self.log = time_log
        self.format = '%m-%d-%Y %H:%M:%S'

    def __call__(self, func):

        def wrapper(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            execution_time = end_time - start_time
            memory_usage = get_process_memory_usage()
            
            # Log the execution details
            log_entry = {
                'class': func.__module__,
                'funtion': func.__name__,
                'start_time': strftime(self.format, localtime(start_time)),
                'end_time': strftime(self.format, localtime(end_time)),
                'execution_time': execution_time,
                'memory_usage': memory_usage
            }
            self.log = pd.concat([self.log, pd.DataFrame([log_entry])], axis=0, ignore_index=True)
            return result
        return wrapper
    
timer = GetFuncExecutionTime()