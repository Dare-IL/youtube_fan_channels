from box import Box
import sys, string, os
import datetime
import pandas as pd

def read_config(config_name: str) -> Box:
    '''
    Read from a file e.g. config.yaml in the current
    directory.

    Args: name of config file (must be .yml or .yaml)
    Returns: Box object of config

    '''
    
    config_path = os.getcwd() + '/' + config_name
    config_file = Box()
    config_file.merge_update(Box.from_yaml(filename=config_path))

    return config_file


def make_data_dirs(channel: str) -> string:   
    '''
    Create data directory for channel
    Args: channel name
    '''  

    # check if data directory exits if not create
    if not os.path.isdir('./data'):
        os.system("mkdir data")

    dir = f'./data/{channel}'

    # check if channel directory exits if not create
    if not os.path.isdir(dir):
        os.system(f"mkdir {dir}")
    
    return dir

def split_date_yearly(start, end):
    '''
    Split date range into yearly chunks so we can delta load
    YT only allows 10K api calls a day. Therefore a large
    date range may exceed daily limit

    Returns:
        date_range: list of start-end in yearly chunks
    
    '''        
    # convert start to correct format
    start_date = datetime.datetime.strptime(start, '%Y%m%d').isoformat('T') + 'Z'

    # convert dates to datetime
    start = datetime.datetime.strptime(start, '%Y%m%d')
    if end:
        end = datetime.datetime.strptime(end, '%Y%m%d')
    else:
        end = datetime.date.today().strftime('%Y%m%d') 
        end = datetime.datetime.strptime(end, '%Y%m%d')   
    
    # initialise list with start
    date_range = [start_date]
    # initialise next year as start 
    next_year = start 

    while next_year < end:
        
        # + 1 year as next year
        next_year += pd.DateOffset(years=1)

        # if next year is greater than end, then take end
        if next_year > end:            
            date_range.append(end.isoformat('T') + 'Z')
        else:        
        # else add next year to list
            date_range.append(next_year.isoformat('T') + 'Z')

    return date_range        
