import os, sys
import typing
import requests
import json
from tqdm import tqdm

'''
Thanks to python engineer for the useful tutorial
https://www.youtube.com/watch?v=5qtC-tsQ-wE
'''


class ChannelStats:

    def __init__(self, api_key: str, channel_id: str, start_date: str, end_date: str) -> None:
        self.api_key = api_key
        self.channel_id = channel_id
        self.start_date = start_date
        self.end_date = end_date
        self.channel_stats = None
        self.video_data = None

    def get_channel_stats(self):
        '''
        Get the overall statistics for a single YT channel
        '''
        
        # set url 
        base_url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'    
        
        # make get request
        json_url = requests.get(base_url)

        # get data from json
        data = json.loads(json_url.text)
        
        # get statistics
        self.channel_stats = data["items"][0]["statistics"]
        return self.channel_stats

    def get_video_data(self):
        '''
        Get the data for YT videos.
        1. Get video IDs using search endpoint
        2. Get video stats using video endpoint

        '''
        # get video ids
        videos = self._get_all_video_ids()
        #print(videos)

        # get video data
        for video_id in tqdm(videos.keys()):
            video_data = self._get_single_video_data(video_id)
            videos[video_id] = video_data

        self.video_data = videos    

        return


    def _get_single_video_data(self, video_id):
        '''
        Get data for a single video. Uses snippet and statistics part
        Args:
            video_id: ID for single video
        Returns:
            xxxx: dict of data    
        '''
        base_url = f'https://www.googleapis.com/youtube/v3/videos?key={self.api_key}&channelId={self.channel_id}&id={video_id}&part=snippet,statistics'
        json_url = requests.get(base_url)
        json_data = json.loads(json_url.text)
        # print(json_data)
        # sys.exit('chill')

        return json_data['items']
 


    
    def _get_all_video_ids(self):
        '''
        Api returns a max of 50 results per page so we need to iterate over all pages
        Returns: dict of all videos IDs after specified start date

        '''
        print(f'Get videos from {self.start_date} - {self.end_date}')
        base_url = f'https://www.googleapis.com/youtube/v3/search?part=id&order=date&channelId={self.channel_id}&key={self.api_key}&maxResults=50&publishedAfter={self.start_date}&publishedBefore={self.end_date}' 
        # base_url = f'https://www.googleapis.com/youtube/v3/search?part=id&order=date&channelId={self.channel_id}&key={self.api_key}&maxResults=50'          


        channel_videos, npt = self._get_video_ids_per_page(base_url)

        # NOTE: avoid infinite loop
        while npt:
            next_page_url = base_url + '&pageToken=' + npt
            page_videos, npt = self._get_video_ids_per_page(next_page_url)
            channel_videos.update(page_videos)            


        return channel_videos

    def _get_video_ids_per_page(self, url):
        '''
        Get all video IDs on one results page (max is 50 results per page)
        Args:
            url: url to request. May contain parameters for the next page
        Returns:
            page_video_ids: dict of video IDs for current results page
            nextPage: token for next page or None
        '''  

        json_url = requests.get(url)
        data = json.loads(json_url.text)
        page_video_ids = dict()

        try:
            item_data = data['items']
        except KeyError:
            print(f'Daily limit might be exceeded') 
            print(data['error'])
            sys.exit('stop')
            

        nextPage = data.get('nextPageToken', None)

        for item in item_data:
            kind = item['id']['kind']
            #print(kind)
            if kind == 'youtube#video':
                video_id = item['id']['videoId']
                page_video_ids[video_id] = dict()

        return page_video_ids, nextPage        

    
    def save_channel_stats_json(self, save_name: str, save_dir: str, start_date: str, end_date:str):
        
        start = start_date[:10].replace("-","")
        end = end_date[:10].replace("-","")
        file_name = f'{save_name}_{start}_{end}.json'
        save_path = save_dir + '/' + file_name

        if self.channel_stats and self.video_data:
            total_data = {'channel_stats': self.channel_stats,
             'video_date': self.video_data}
            with open(save_path, 'w') as f:
                json.dump(total_data, f, indent=4)

        return        
