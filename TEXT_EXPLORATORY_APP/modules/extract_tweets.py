import requests
import os
import json
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import time



def create_url(query = None,until_id=None,since_id=None):
    
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
        
        url = "https://api.twitter.com/2/tweets/search/recent?query={}&max_results=100&tweet.fields=author_id,created_at&until_id={}&".format(
            query,until_id
        )

    elif since_id:

        url = "https://api.twitter.com/2/tweets/search/recent?query={}&max_results=100&tweet.fields=author_id,created_at&since_id={}&".format(
            query,since_id
        )

        
    else:
        
        url = "https://api.twitter.com/2/tweets/search/recent?query={}&max_results=100&tweet.fields=author_id,created_at".format(
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


def extract_100_tweets(query = None,until_id=None,since_id=None,key_twitter = None):
    bearer_token = key_twitter
    
    if not until_id:
        
        url = create_url(query,until_id = until_id)
        
    elif not since_id:
        
        url = create_url(query,since_id = since_id)
        
    else:
        
        url = create_url(query = query)
    
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    data_tweets = json.dumps(json_response, indent=4, sort_keys=True)
    return json_response

def extract_many_tweets(qnt_cycle=10,
                        folder="data_tweets",
                        until_id=None,
                        since_id=None,
                        query="@BBB",
                        bearer_token = None,
                        df_concat_path=None):


    if since_id:

        data_tweets_recent = extract_100_tweets(query = "{} -is:retweet".format(query),
                                                since_id=since_id,
                                               key_twitter = bearer_token)
        '''
        time.sleep(1)

        oldest_id = data_tweets_recent['meta']['oldest_id']

        newest_id = data_tweets_recent['meta']['newest_id']

        if df_concat_path:

            df_data_tweets_old = pd.read_csv(df_concat_path)

            df_data_tweets = pd.concat([data_tweets_recent,df_data_tweets_old])

        else:

            df_data_tweets = data_tweets_recent


        name_file = "{}/running/persist_tweets.csv".format(folder)

        # persist base
                
        df_data_tweets.to_csv(name_file,sep=",")
        '''
        
        data = {
                'data':data_tweets_recent["data"],
                'meta': {'newest_id': data_tweets_recent["meta"]["newest_id"],
                        'oldest_id': data_tweets_recent["meta"]["oldest_id"],'query':query}
                }       
        
    else:

        
        oldest_id = None

        newest_id = None
        
        for i in tqdm(range(qnt_cycle)):
        
            
            if i == 0:
                
                #extract the 100 tweets first
                
                if not until_id:
            
                    data_tweets = extract_100_tweets(query = "{} -is:retweet".format(query),until_id=None,key_twitter = bearer_token)
                    time.sleep(1)
                
                else:
                    
                    data_tweets = extract_100_tweets(query = "{} -is:retweet".format(query),until_id=until_id,key_twitter = bearer_token)
                    time.sleep(1)
                    
                
                df_data_tweets_temp = pd.DataFrame(data_tweets["data"])
                
                #get the current date
                
                
                oldest_id = data_tweets['meta']['oldest_id']

                newest_id = data_tweets['meta']['newest_id']
                
                df_data_tweets = df_data_tweets_temp.copy()
                
                # name file
                
                #date_extraction_str = str(date_extraction).replace(".","-").replace(":","-").replace(" ","-")
                
                #name_file = "{}/persist_tweets_{}_{}.csv".format(folder,date_extraction_str,date_extraction_str)
                
                #name_file = "{}/running/persist_tweets.csv".format(folder)

                # persist base
                
                #df_data_tweets.to_csv(name_file,sep=",")
                
        
                
            else:
                
                
                #extract more 100 tweets older

                data_tweets_temp = extract_100_tweets(query = "{} -is:retweet".format(query),until_id=oldest_id,key_twitter = bearer_token)
                time.sleep(1)
                
                df_data_tweets_temp = pd.DataFrame(data_tweets_temp["data"])
                
                
                #get the current date
                
                
                
                oldest_id = data_tweets_temp['meta']['oldest_id']
                
                df_data_tweets = pd.concat([df_data_tweets,df_data_tweets_temp.copy()])

                
                df_data_tweets.reset_index(inplace=True,drop=True)
                
                
                # remove old files
                
                #os.remove(name_file)
                
                
                # name file
                
                #oldest_date_str = str(oldest_date).replace(".","-").replace(":","-").replace(" ","-")
                
                #date_extraction_str = str(date_extraction).replace(".","-").replace(":","-").replace(" ","-")
                
                
                #name_file = "{}/persist_tweets_{}_{}.csv".format(folder,oldest_date_str,date_extraction_str)

                #name_file = "{}/running/persist_tweets.csv".format(folder)
                
                # persist base
                
                #df_data_tweets.to_csv(name_file.format(folder),sep=",")
                
    
        data = {
                'data':df_data_tweets.to_dict("records"),
                'meta': {'newest_id': newest_id,
                        'oldest_id': oldest_id,'query':query}
                }

    #status_system = {'df_concat_path':name_file,'newest_id':newest_id,'oldest_id':oldest_id,'query':query}

    #f_status_system = open("{}/running/status_system.json".format(folder), 'w')
    #json.dump(status_system, f_status_system)


    print("\n")
    print("\n")
    print("data at function")
    data["meta"]["query"]
    print("\n")
    print("\n")
    
    return data
    
    