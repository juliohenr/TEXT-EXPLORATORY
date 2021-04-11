import requests
import json
import os
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

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