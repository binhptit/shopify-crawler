import time 
import logging

def time_log(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        logging.info(f"Start {func.__name__}-------------------------------")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Time of {func.__name__} is {end_time - start_time} seconds\n")

        return result
    
    return wrapper