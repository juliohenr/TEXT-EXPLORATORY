from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import os
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from os import path
from PIL import Image
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from nltk.corpus import stopwords
from unicodedata import normalize as norm
from .modules.api_keys import BEARER_TOKEN
from django.views.decorators.csrf import csrf_exempt
from .modules.toolkit_dash import *
from .modules.extract_tweets import *
import shutil

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(LOCAL_PATH,"dataset_pocah.csv")

IMAGE_PATH = os.path.join(LOCAL_PATH,"static" + os.sep + "css" + os.sep + "word_cloud.png")

PERSIST_DATA_TWEET_PATH = os.path.join(LOCAL_PATH,"data_tweets")

PERSIST_DATA_TWEET_PATH_BACKUP = os.path.join(LOCAL_PATH,"data_tweets" + os.sep + "backup")

PERSIST_DATA_TWEET_PATH_RUNNING = os.path.join(LOCAL_PATH,"data_tweets" + os.sep + "running")


#___________________________________________________________________________________________________________________________________________________________
#ROTA PARA RENDERIZAR O DASHBOARD



files = os.listdir(PERSIST_DATA_TWEET_PATH_RUNNING)

for f in files:

    try:

        os.remove(os.path.join(PERSIST_DATA_TWEET_PATH_BACKUP,f))

    except:

        shutil.move( os.path.join(PERSIST_DATA_TWEET_PATH_RUNNING,f) , PERSIST_DATA_TWEET_PATH_BACKUP)


def index (request):

    try:

        data_tweets_final = pd.read_csv(PERSIST_DATA_TWEET_PATH + os.sep +"running" + os.sep + "persist_tweets.csv")

        try:

            with open(PERSIST_DATA_TWEET_PATH + os.sep +"running" + os.sep + 'status_system.json') as f:

                status_system_data = json.load(f)

                status_system = status_system_data["status"]

                print("\n")
                print("\n")
                print(status_system)
                print("\n")
                print("\n")
        

        except:

                status_system = "Stopped"



        #status_load = json.load(PERSIST_DATA_TWEET_PATH + os.sep +"running" + os.sep + "persist_tweets.csv")



        stop_words_domain=["não","da","globoplay",
                            "só","pra","vc","pois","lá","outro",
                            "outra","vou","vão","assim","outro",
                            "outra","ter","ver","agora","hoje",
                            "tudo","todos","todo","ah","acho",
                            "achamos","né","ser","vai","alguma",
                            "mas","porém","entretanto",
                            "faz","fazemos","farão",
                            "tbm","fazia","tá","tb","ia",
                            "ir","to","nela","nele","nelas",
                            "neles","naquele","naquueles",
                            "naquelas","naquela","coisa","mim",
                            "tô","aí","n",
                            "pro","é","dessa","vamos","q",
                            "desse","tava","msm","vamo","que","porque",
                            "nem","mano","manos","caras","xd","kkkk","pq","por","cara",
                            "gente","dar","sobre","tão","toda","vezes",
                            "então","viu","vemos","pode","podemos","vez",
                            "vcs","hein","quer","sim","deu","já","demos",
                            "todas","aqui","sei","sabemos","fazer","fiz",
                            "fez","fazemos","vem","vamos","ainda","tanto","nesse","pocah"]

        data_tweets_final["text"] = data_tweets_final["text"].apply(lambda x: text_cleaner(text=x,stop_words_domain=stop_words_domain)) 

        #EXTRACT DATA TO PLOT DASHBOARD

        # Criação de uma coluna com os textos sem repetição de palavras para ser utilizado na análise exploratória

        data_tweets_final['text_unique_words'] = data_tweets_final['text'].apply(lambda x: convert_text_to_no_repeat_words(x))

        # Calculo Número de tokens

        data_tweets_final['number_tokens'] = data_tweets_final['text'].apply(lambda x: calculate_number_words(x))

        # Calculo Número de diferentes tokens

        data_tweets_final['number_diferent_tokens'] = data_tweets_final['text'].apply(lambda x: calculate_number_diferent_words(x))

        # Máximo número de tokens 

        max_count = data_tweets_final["number_tokens"].max()

        # Mínimo número de tokens 

        min_count = data_tweets_final["number_tokens"].min()

        # Máximo número de tokens diferentes 

        max_count_diferents_tokens = data_tweets_final["number_diferent_tokens"].max()

        # Mínimo número de tokens diferentes 

        min_count_diferents_tokens = data_tweets_final["number_diferent_tokens"].min()

        #__________________________

        # Média número de tokens 

        mean_count = data_tweets_final["number_tokens"].mean()

        # Média número de tokens diferentes 

        mean_count_diferents_tokens = data_tweets_final["number_diferent_tokens"].mean()

        #__________________________

        # STD número de tokens 

        std_count = data_tweets_final["number_tokens"].std()

        # STD número de tokens diferentes 

        std_count_diferents_tokens = data_tweets_final["number_diferent_tokens"].std()

        #___________________________

        # Mediana número de tokens 

        median_count = data_tweets_final["number_tokens"].median()

        # Mediana número de tokens diferentes 

        median_count_diferents_tokens = data_tweets_final["number_diferent_tokens"].median()

        #____________________________

        # Variância número de tokens 

        var_count = data_tweets_final["number_tokens"].var()

        # Variância número de tokens diferentes 

        var_count_diferents_tokens = data_tweets_final["number_diferent_tokens"].var()

        #____________________________

        #top variable

        top = 30

        #Numero de bins para o histograma

        n_bins = 40

        ## Dados para o histograma do number_tokens

        data_tweets_final['bins'] = data_tweets_final['number_tokens'].apply(lambda x: function_to_calc_histogram(x,initial_interval = min_count, final_interval = max_count,n_bins = n_bins,indice=False))

        data_tweets_final['indices_bins'] = data_tweets_final['number_tokens'].apply(lambda x: function_to_calc_histogram(x,initial_interval = min_count, final_interval = max_count,n_bins = n_bins,indice=True))

        data_histogram_words = data_tweets_final.groupby(["bins","indices_bins"]).sum().sort_values(by=["indices_bins"])

        data_histogram_words.reset_index(drop=False,inplace=True)

        ## Dados para o histograma do number_diferent_tokens

        data_tweets_final['bins_diferent_tokens'] = data_tweets_final['number_diferent_tokens'].apply(lambda x: function_to_calc_histogram(x,initial_interval = min_count_diferents_tokens, final_interval = max_count_diferents_tokens,n_bins = n_bins,indice=False))

        data_tweets_final['indices_bins_diferent_tokens'] = data_tweets_final['number_diferent_tokens'].apply(lambda x: function_to_calc_histogram(x,initial_interval = min_count_diferents_tokens, final_interval = max_count_diferents_tokens,n_bins = n_bins,indice=True))

        data_histogram_diferent_words = data_tweets_final.groupby(["bins_diferent_tokens","indices_bins_diferent_tokens"]).sum().sort_values(by=["indices_bins_diferent_tokens"])

        data_histogram_diferent_words.reset_index(drop=False,inplace=True)

        # DF top 10 MEAN

        df_report_mean = plot_bar_count_words(text_column='text',
                                                        dataframe=data_tweets_final,
                                                        metric='MEAN',top=top,return_df=True)
        # DF top 10 SUM

        df_report_sum = plot_bar_count_words(text_column='text',
                                                        dataframe=data_tweets_final,
                                                        metric='SUM',top=top,return_df=True)
        # DF top 10 MEAN TF-IDF

        df_report_tfidf_mean = plot_bar_tf_idf(text_column='text',
                                                        dataframe=data_tweets_final,
                                                        metric='MEAN',top=top,return_df=True)
        # DF top 10 MAX TF-IDF

        df_report_tfidf_max = plot_bar_tf_idf(text_column='text',
                                                        dataframe=data_tweets_final,
                                                        metric='MAX',top=top,return_df=True)

        # DF top 10 SUM docs

        df_report_sum_docs = plot_bar_count_words(text_column='text_unique_words',
                                                        dataframe=data_tweets_final,
                                                        metric='SUM',top=top,return_df=True)

        df_report_sum_docs["P_DOCS"] =  (df_report_sum_docs["SUM"]/len(data_tweets_final))*100

        data = {
            "mean_count_results":df_report_mean["MEAN"].tolist(),
            "mean_count_words": json.dumps(df_report_mean["WORDS"].tolist()),
            "sum_count_results":df_report_sum["SUM"].tolist(),
            "sum_count_words":df_report_sum["WORDS"].tolist(),
            "tfidf_mean_results":df_report_tfidf_mean["MEAN"].tolist(),
            "tfidf_mean_words":df_report_tfidf_mean["WORDS"].tolist(),
            "tfidf_max_results":df_report_tfidf_max["MAX"].tolist(),
            "tfidf_max_words":df_report_tfidf_max["WORDS"].tolist(),
            "histogram_bins_diferent_tokens":data_histogram_diferent_words["bins_diferent_tokens"].tolist(),
            "histogram_number_diferent_tokens":data_histogram_diferent_words["number_diferent_tokens"].tolist(),
            "histogram_bins_number_tokens":data_histogram_words["bins"].tolist(),
            "histogram_number_tokens":data_histogram_words["number_tokens"].tolist(),
            "number_of_docs": df_report_sum_docs["SUM"].tolist(),
            "p_number_of_docs": df_report_sum_docs["P_DOCS"].tolist(),
            "words_number_of_docs": df_report_sum_docs["WORDS"].tolist(),
            "median_count":median_count,
            "median_count_diferents_tokens":median_count_diferents_tokens,
            "mean_count":mean_count,
            "mean_count_diferents_tokens":mean_count_diferents_tokens,
            "std_count":std_count,
            "std_count_diferents_tokens":std_count_diferents_tokens,
            "var_count":var_count,
            "var_count_diferents_tokens":var_count_diferents_tokens,
            "status_system":status_system
        }


        text = " ".join(review for review in data_tweets_final.text)

        wordcloud = WordCloud(max_font_size=300, max_words=70, background_color="black",width=3000, height=1300).generate(text)

        wordcloud.to_file(IMAGE_PATH)

    
    except:


        data = {
            "mean_count_results":[0,0,0,0,0,0,0,0,0,0],
            "mean_count_words": ["palavra1","palavra2","palavra3","palavra4","palavra5","palavra6","palavra7","palavra8","palavra9","palavra10"],
            "sum_count_results":[0,0,0,0,0,0,0,0,0,0],
            "sum_count_words":["palavra1","palavra2","palavra3","palavra4","palavra5","palavra6","palavra7","palavra8","palavra9","palavra10"],
            "tfidf_mean_results":[0,0,0,0,0,0,0,0,0,0],
            "tfidf_mean_words":["palavra1","palavra2","palavra3","palavra4","palavra5","palavra6","palavra7","palavra8","palavra9","palavra10"],
            "tfidf_max_results":[0,0,0,0,0,0,0,0,0,0],
            "tfidf_max_words":["palavra1","palavra2","palavra3","palavra4","palavra5","palavra6","palavra7","palavra8","palavra9","palavra10"],
            "histogram_bins_diferent_tokens":["bin1","bin2","bin3","bin4","bin5","bin6","bin7","bin8","bin9","bin10"],
            "histogram_number_diferent_tokens":[0,0,0,0,0,0,0,0,0,0],
            "histogram_bins_number_tokens":["bin1","bin2","bin3","bin4","bin5","bin6","bin7","bin8","bin9","bin10"],
            "histogram_number_tokens":[0,0,0,0,0,0,0,0,0,0],
            "number_of_docs": [0,0,0,0,0,0,0,0,0,0],
            "p_number_of_docs": [0,0,0,0,0,0,0,0,0,0],
            "words_number_of_docs": ["palavra1","palavra2","palavra3","palavra4","palavra5","palavra6","palavra7","palavra8","palavra9","palavra10"],
            "median_count":0,
            "median_count_diferents_tokens":0,
            "mean_count":0,
            "mean_count_diferents_tokens":0,
            "std_count":0,
            "std_count_diferents_tokens":0,
            "var_count":0,
            "var_count_diferents_tokens":0,
            "status_system":"Stopped"
        }


    
    return render(request,"index.html",data)


#___________________________________________________________________________________________________________________________________________________________
#ROTA PARA PERSISTIR OS DADOS
@csrf_exempt 
def persist_results (request):

    data = json.loads(json.dumps(request.POST))

    print("\n")
    print("\n")
    print("\n")
    print("data: \n")
    print(data)
    print("\n")
    print("\n")
    print("\n")

    #data["contentTwitter"]
    
    data_tweets_final = extract_many_tweets(qnt_cycle=1,folder=PERSIST_DATA_TWEET_PATH,query="bbb",bearer_token = BEARER_TOKEN)

    print("\n")
    print("\n")

    print(data_tweets_final)

    print("\n")
    print("\n")

    f_data = open(PERSIST_DATA_TWEET_PATH + os.sep +"running" + os.sep + "data_tweets.json", 'w+', encoding='utf8')



    json.dump(data_tweets_final, f_data, ensure_ascii=False)




    status_system = {'status':data["status_sytem"]}

    f_status_system = open("{}/running/status_system.json".format(PERSIST_DATA_TWEET_PATH), 'w')
    
    
    json.dump(status_system, f_status_system)



    
    # LOAD STATUS SYSTEM
    '''
    file_name = open(PERSIST_DATA_TWEET_PATH + os.sep +"running" + os.sep + "status_system.json", 'r')
    
    data_json_status = json.load(file_name)

    print("\n")
    print("\n")
    print(data_json_status["query"])
    print("\n")
    print("\n")    
    '''
    



    return HttpResponse("status: okay")

