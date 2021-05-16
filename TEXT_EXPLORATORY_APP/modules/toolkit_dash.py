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
import datetime
from datetime import timedelta
nltk.download('stopwords')


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


def modify_date(x):
    

    date_time_str = x.replace("T"," ").replace("Z","")
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    return date_time_obj - timedelta(hours=3)
    

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



### Função para o pré-processamento do texto 


def text_cleaner(text,stop_words_domain =None):

    

    try:
        nltk_stopwords =  stopwords.words('portuguese') + stop_words_domain

        nltk_stopwords_processed = [norm('NFKD', i).encode('ascii', 'ignore').decode().lower() for i in nltk_stopwords]

    except:
        nltk_stopwords = stopwords.words('portuguese')

    regex_stop_words = '|'.join(nltk_stopwords)

    
    regex_remove_https = 'https([a-zA-Zà-úÀ-Ú0-9]|[-()\#/@;:<>{}`+=~|.!?,])+'


    text_without_https = re.sub(r"(\s|^){0}(\s{0})*($|\s)".format(regex_remove_https)," ",text)


    text_without_special_caracteres = re.sub(r"[^a-zA-ZÀ-Úà-ú]+"," ",text_without_https)

    text_without_alone_caractere = re.sub(r"\s[a-zA-ZÀ-Úà-ú]\s|\s[a-zA-ZÀ-Úà-ú]$|^[a-zA-ZÀ-Úà-ú]\s"," ",text_without_special_caracteres)
    

    text_pattern_space = re.sub(r"\s+"," ",text_without_alone_caractere)

    
    text_split = text_pattern_space.split(" ")

    
    text_list = [i for i in text_split  if norm('NFKD', i).encode('ascii', 'ignore').decode().lower() not in nltk_stopwords_processed]


    text_final = " ".join(text_list)


    


    return text_final
