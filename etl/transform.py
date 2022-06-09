import os, sys
import typing
import json
import pandas as pd

def video_json_to_csv(channel: str, save_dir: str) -> None:
    '''
    Read json files and create dataframe
    output csv with following columns:
    title, date, viewCount, likeCount, commentCount
    '''
    
    ids, date, likes, views, comments, title = [], [], [], [], [], []

    # TODO: read in all json files in dir
    for file in os.listdir(save_dir + '/'):
        if file.endswith('.json'):
            with open(save_dir + '/' + file, 'r') as f:
                json_data = json.load(f)
                video_info = json_data['video_date'] 
                video_id = list(video_info.keys()) 
                ids.append(video_id)

                for vid in video_info:
                    date.append(video_info[vid][0]['snippet']['publishedAt'])
                    title.append(video_info[vid][0]['snippet']['title'])
                    views.append(video_info[vid][0]['statistics'].get('viewCount', None))
                    likes.append(video_info[vid][0]['statistics'].get('likeCount', None))
                    comments.append(video_info[vid][0]['statistics'].get('commentCount', None)) 
    

    data_table = pd.DataFrame({
                                'title': title,
                                'date': date,
                                'views': views,
                                'likes': likes,
                                'comments': comments

    }) 

    save_path = save_dir + '/' + channel + '_transform.csv'
    
    data_table.to_csv(save_path, index=False) 

    return    
  