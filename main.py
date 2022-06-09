from modulefinder import EXTENDED_ARG
import os, sys
import click
from dotenv import load_dotenv
from datetime import datetime, time

from pandas import date_range
from etl.extract import ChannelStats
from etl.transform import video_json_to_csv
from analyse.preprocess import clean_date_scores
from helpers import read_config, make_data_dirs, split_date_yearly

load_dotenv()
api_key = os.getenv('api_key')


@click.command()
@click.option('--channel_name',  type=click.Choice(['aftv', 'tus', 'expressions']), help='channel name', default='expressions')
@click.option('--start', help='date video published after', default='20220101')
@click.option('--end', help='date video published before', default=None)
@click.option('--config', help='configuration file', default='config.yml')
def main(channel_name: str, start: str, end: str, config: str):    
    
    # if end date specified ensure it is later than start date
    if end:        
        if start > end:
            sys.exit('start_date cannot be later than end_date')
    # else:
    #     end_date = datetime.datetime.today().strftime("%Y%m%d%H:%M:%S")         

    # read config
    config = read_config(config)   

    # make data directories to store extracted data
    save_dir = make_data_dirs(channel_name)

    date_range = split_date_yearly(start, end)

    print(date_range)
    # sys.exit('chill')

    # execute pipeline steps (extract, transform, ...)

    # 1. Extract: get data from YT api
    if 'extract' in config.pipeline_steps and config.pipeline_steps.extract: 
        for i in range(len(date_range)-1):
            start_date = date_range[i]
            end_date = date_range[i+1]
            channel = ChannelStats(api_key,config['channel_names'][channel_name], start_date, end_date)
            channel.get_channel_stats() # subscriber count, video count etc
            channel.get_video_data() # get videos within specified time range
            channel.save_channel_stats_json(channel_name, save_dir, start_date, end_date)
    else:
        print('Skipping data extract')    

    # 2. Transform: get data video data from json and save as csv
    if 'transform' in config.pipeline_steps and config.pipeline_steps.transform: 
        video_json_to_csv(channel_name, save_dir)
    else:
        print('Skipping json transform to csv') 

    # 3. Preprocess: get dates and scores
    if 'preprocess' in config.pipeline_steps and config.pipeline_steps.preprocess: 
        clean_date_scores(channel_name, config['team_names'][channel_name], save_dir)
    else:
        print('Skipping preprocess step')        


if __name__ == '__main__':
    main()