'''
This script takes a directory of Allrecipes.com html files (created using the "allrecipes_scraper.py" file also in this Github repository), uses BeautifulSoup to find the 'script' tags with page data and nutrition information, loads the data into a json file, and then concatenates the json files into a Pandas dataframe.

By Kaelynn Rose 2/25/21

'''

import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from joblib import Parallel,delayed
import os

################ USER INPUT #################

directory = '/Users/kaelynnrose/Documents/GALVANIZE/Capstones/Capstone_1/test' # path to directory of .html files to parse into dataframe
output = '/Users/kaelynnrose/Documents/GALVANIZE/Capstones/Capstone_1/dataframetest.csv' # path to store newly created dataframe


############## END USER INPUT ###############


df = pd.DataFrame() # initialize a blank dataframe to populate

def create_dataframe(directory,output,df):
    for filename in os.listdir(directory): # loop through list of files in the specified directory
        fname = os.path.join(directory,filename)
        with open(fname, 'r') as f:
            try:
                print('Working on file ' + str(filename))
                soup = BeautifulSoup(f.read(),'html.parser') # parse html with Beautifulsoup
                
                text1 = str(soup.find_all('script',type='application/ld+json')[0]) # find 'script' tags in html file with the type='application/ld+json', this is the main source of information on each recipe page
                text_r1 = text1.split('<script type="application/ld+json">')[1].split('</script>')[0] # format to be read by json.loads
                text2 = str(soup.find_all('script',id="universal-data-layer")[0]) # find 'script' tags in html file with the id="universal-data-layer", this has extra information on recipe created date and nlp data from allrecipes.com
                text_r2 = text2.split('<script id="universal-data-layer">')[1].split('</script>')[0] # remove html tags

                # add a few extra columns with data from text2
                inddate = text_r2.find('created_date')
                createddate = text_r2[inddate+16:inddate+36]
                indnlp = text_r2.find('nlp_sentiment_label')
                nlp_sentiment_label = text_r2[indnlp+23:indnlp+31]
                indnlp2 = text_r2.find('nlp_sentiment_score')
                nlp_sentiment_score = text_r2[indnlp2+22:indnlp2+25]
                indnlp3 = text_r2.find('nlp_sentiment_magnitude')
                nlp_sentiment_magnitude = text_r2[indnlp3+26:indnlp3+29]
                
                # load and normalize main json file with the bulk of the data columns
                j_file = json.loads(text_r1)
                df_line = pd.json_normalize(j_file)
 
                # add these extra columns from the id='universal-data-layer' tag to the dataframe
                df_line['created_date'] = createddate
                df_line['nlp_sentiment_label'] = nlp_sentiment_label
                df_line['nlp_sentiment_score'] = nlp_sentiment_score
                df_line['nlp_sentiment_magnitude'] = nlp_sentiment_magnitude

                # add the new line of the dataframe to the main dataframe
                df = pd.concat([df,df_line.iloc[1:,:]],ignore_index=True) # add the new line to the dataframe
                
            except:
                print(f'Bad html file. Did not add any data to dataframe.')

    df.to_csv(output) # export the dataframe to a .csv file


# Create dataframe
create_dataframe(directory,output,df)
