import re
import pandas as pd

def get_scores(video_title: str, team: str) -> int:
    '''
    
    Args:
        video_title: title of YT video
        team: name of team

    Returns:
        team score: int or None if title doesn't contain score
        opponent score:  int or None if title doesn't contain score  

    '''
    # make lower case, remove spaces and 'hotspur'
    team_name = team.lower().replace(" ", "").replace('hotspur', '')
    title = video_title.lower().replace(" ", "").replace('hotspur', '').replace('manunited', 'manchesterunited')

    # look for a pattern like 1-0, 2-1, etc
    pattern = re.compile(r"\d\D\d")
    match = pattern.search(title)

    # if video title does not contain scores return nothing
    if not match:
        return None, None

    # get scores for home and away teams. Home team is always on the left
    home_score, away_score = int(title[match.start()]), int(title[match.end()-1])

    # find home team. If team name is to the left of 2-1 pattern then team is home team
    start_id = match.start()-len(team_name)
    home_team_name = title[start_id:match.start()]
    is_home_team = team_name == home_team_name

    if is_home_team:
        return home_score, away_score
    else:
        return away_score, home_score  


def clean_date_scores(channel_name, team_name, save_dir): 
    '''
    Convert date to pandas datetime
    create column for team and opponent scores
    save final data frame as channel_name_preprocess.csv
    
    '''   
    read_name = save_dir + '/' + channel_name + '_transform.csv'
    save_name = save_dir + '/' + channel_name + '_preprocess.csv'    

    df = pd.read_csv(read_name)

    # convert date format
    df['date'] = pd.to_datetime(df['date']).dt.date

    scores = df.apply(lambda x: get_scores(x['title'], team_name), axis=1, result_type='expand')
    df['team_score'], df['opponent_score'] = scores[0], scores[1]
    df.to_csv(save_name, index=False)


