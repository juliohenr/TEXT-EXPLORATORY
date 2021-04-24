
import requests
import os
import json
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import time



def create_url(query = None,until_id=None):
    
    #query = "@BBB -is:retweet"
    #"from:twitterdev -is:retweet"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    
    if until_id:
        
        url = "https://api.twitter.com/2/tweets/search/recent?query={}&max_results=10&tweet.fields=author_id,created_at&until_id={}&".format(
            query,until_id
        )
        
    else:
        
        url = "https://api.twitter.com/2/tweets/search/recent?query={}&max_results=10&tweet.fields=author_id,created_at".format(
            query
        )
            
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def extract_100_tweets(query = None,until_id=None,key_twitter = None):
    bearer_token = key_twitter
    url = create_url(query,until_id)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    data_tweets = json.dumps(json_response, indent=4, sort_keys=True)
    return json_response

def extract_many_tweets(qnt_cycle=10,folder="data_tweets",start_from_id=None,query="@BBB",bearer_token = None):
    
    
    oldest_id = None
    
    for i in tqdm(range(qnt_cycle)):
    
        
        if i == 0:
            
            #extract the 100 tweets first
            
            if start_from_id:
        
                data_tweets = extract_100_tweets(query = "{} -is:retweet".format(query),until_id=None,key_twitter = bearer_token)
                time.sleep(1)
            
            else:
                
                data_tweets = extract_100_tweets(query = "{} -is:retweet".format(query),until_id=start_from_id,key_twitter = bearer_token)
                time.sleep(1)
                
            
            df_data_tweets_temp = pd.DataFrame(data_tweets["data"])
            
            #get the current date
            
            date_extraction = datetime.now()
            
            df_data_tweets_temp["date_extraction"] = date_extraction 
            
            
            oldest_id = data_tweets['meta']['oldest_id']
            
            oldest_date = date_extraction
            
            df_data_tweets = df_data_tweets_temp.copy()
            
            # name file
            
            date_extraction_str = str(date_extraction).replace(".","-").replace(":","-").replace(" ","-")
            
            #name_file = "{}/persist_tweets_{}_{}.csv".format(folder,date_extraction_str,date_extraction_str)
            
            name_file = "{}/persist_tweets.csv".format(folder)

            # persist base
            
            df_data_tweets.to_csv(name_file,sep=",")
            
    
            
        else:
            
            
            #extract more 100 tweets older

            data_tweets_temp = extract_100_tweets(query = "{} -is:retweet".format(query),until_id=oldest_id,key_twitter = bearer_token)
            time.sleep(1)
            
            df_data_tweets_temp = pd.DataFrame(data_tweets_temp["data"])
            
            
            #get the current date
            
            
            date_extraction = datetime.now()
            
            df_data_tweets_temp["date_extraction"] = date_extraction 
            
            oldest_id = data_tweets_temp['meta']['oldest_id']
            
            df_data_tweets = pd.concat([df_data_tweets,df_data_tweets_temp.copy()])
            
            date_extraction = datetime.now()
            
            df_data_tweets.reset_index(inplace=True,drop=True)
            
            
            # remove old files
            
            os.remove(name_file)
            
            
            # name file
            
            oldest_date_str = str(oldest_date).replace(".","-").replace(":","-").replace(" ","-")
            
            date_extraction_str = str(date_extraction).replace(".","-").replace(":","-").replace(" ","-")
            
            
            #name_file = "{}/persist_tweets_{}_{}.csv".format(folder,oldest_date_str,date_extraction_str)

            name_file = "{}/persist_tweets.csv".format(folder)
            
            # persist base
            
            df_data_tweets.to_csv(name_file.format(folder),sep=",")
            
            

    return df_data_tweets
    
    
