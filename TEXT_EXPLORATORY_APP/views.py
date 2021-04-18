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



LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))


DATA_PATH = os.path.join(LOCAL_PATH,"dataset_tweets_test.csv")


IMAGE_PATH = os.path.join(LOCAL_PATH,"static" + os.sep + "css" + os.sep + "word_cloud.png")


data_tweets_final = pd.read_csv(DATA_PATH)



# Funções (Análise Exploratória)

### Função para plotar bar plot com a contagem de tokens

def plot_bar_count_words(text_column=None,
                         label_column=None,
                         name_class=None,
                         dataframe=None,
                         metric='SUM',
                         top=50,return_df=True):
    
    corpus = dataframe[text_column].values
    
    vectorizer = CountVectorizer()
    data_vect = vectorizer.fit_transform(corpus)
    data_vect = data_vect.toarray()
    
    df_count_words =  pd.DataFrame({
    "WORDS":vectorizer.get_feature_names(),
    "MEAN":data_vect.mean(axis=0),
    "SUM":data_vect.sum(axis=0),
    "STD":data_vect.std(axis=0),
    }) 
    
    

    if return_df:
    
        return df_count_words[[metric,'WORDS']].sort_values(by=[metric],ascending=False)[0:top]
    
    else:
        
        fig = plt.figure(figsize=(15,10))
        
        ax = sns.barplot(x=metric, 
                 y="WORDS", 
                 data=df_count_words[[metric,'WORDS']].sort_values(by=[metric],
                                                                            ascending=False)[0:top])


### Função para plotar bar plot com tf-idf


def plot_bar_tf_idf(text_column=None,
                         label_column=None,
                         name_class=None,
                         dataframe=None,
                         metric='SUM',
                         top=50,return_df=True):
    
    corpus = dataframe[text_column].values
    
    vectorizer = TfidfVectorizer()
    data_vect = vectorizer.fit_transform(corpus)
    data_vect = data_vect.toarray()
    
    df_count_words =  pd.DataFrame({
    "WORDS":vectorizer.get_feature_names(),
    "MEAN":data_vect.mean(axis=0),
    "SUM":data_vect.sum(axis=0),
    "STD":data_vect.std(axis=0),
    "MAX":data_vect.std(axis=0)
    }) 
    
    

    if return_df:
    
        return df_count_words[[metric,'WORDS']].sort_values(by=[metric],ascending=False)[0:top]
    
    else:
        
        fig = plt.figure(figsize=(15,10))
        
        ax = sns.barplot(x=metric, 
                 y="WORDS", 
                 data=df_count_words[[metric,'WORDS']].sort_values(by=[metric],
                                                                            ascending=False)[0:top])

### Função para contagem de tokens

def calculate_number_words(text):

    quantity_of_words = text.split(" ")

    quantity_of_words = [i for i in quantity_of_words if i!=""]

    quantity_of_words = len(quantity_of_words)

    return quantity_of_words


### Função para contagem de diferentes tokens


def calculate_number_diferent_words(text):

    quantity_of_diferent_words = text.split(" ")

    quantity_of_diferent_words = [i for i in quantity_of_diferent_words if i!=""]

    quantity_of_diferent_words = set(quantity_of_diferent_words)

    quantity_of_diferent_words = list(quantity_of_diferent_words)

    quantity_of_diferent_words = len(quantity_of_diferent_words)

    return quantity_of_diferent_words


### Função para criar textos sem repetição de palavras para ser utilizado na análise exploratória 

def convert_text_to_no_repeat_words(text):

    text_with_no_repeat_words = text.split(" ")

    text_with_no_repeat_words = [i for i in text_with_no_repeat_words if i!=""]

    text_with_no_repeat_words = set(text_with_no_repeat_words)

    text_with_no_repeat_words = list(text_with_no_repeat_words)

    text_with_no_repeat_words = " ".join(text_with_no_repeat_words)

    return text_with_no_repeat_words

### Função para o pré-processamento do texto 


def text_cleaner(text):
    
    nltk_stopwords = stopwords.words('portuguese')

    collection_text = [ {"text" : text}]
    text = pd.DataFrame(collection_text)

    text['text'] = text['text'].astype('str')
    text['text'] = text['text'].str.lower()
    text['text'] = text['text'].str.replace('\n',' ')
    text['text'] = text['text'].str.replace('\r',' ')
    text['text'] = text['text'].apply(lambda x: norm('NFKD', x).encode('ascii', 'ignore').decode())
    text['text'] = text['text'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]',' ',x))
    text['text'] = text['text'].apply(lambda x: re.sub(r'\s+',' ',x))
    pat = r'\b(?:{})\b'.format('|'.join(nltk_stopwords))
    text['text'] = text['text'].str.replace(pat,'')
    text = text['text'].values[0]

    return text


# Função para estruturação do dataset que será utilizado no histograma 

def function_to_calc_histogram(x,initial_interval, final_interval,n_bins,indice=False):

    interval = np.linspace(initial_interval, final_interval, num=n_bins)

    for j,i in enumerate(interval):


        if i == interval[len(interval)-1]:

            if x>=i:

                
                if indice:

                    return j
                
                else:
                    
                    return "{}<".format(x)


        else:

            if x>=i and x<interval[j+1]:

                inicial = round(i, 1)

                final = round(interval[j+1],1)

            
                if indice:

                    return j
                
                else:
                    
                    return "[{},{})".format(inicial,final)


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



#____________________________


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



}


text = " ".join(review for review in data_tweets_final.text)

wordcloud = WordCloud(max_font_size=200, max_words=200, background_color="black",width=3000, height=1300).generate(text)

wordcloud.to_file(IMAGE_PATH)





#ROUTES


def index (request):

    #return HttpResponse("<h1>Oi<h1>")

    return render(request,"index.html",data)

