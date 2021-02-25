'''
This code scrapes recipes from AllRecipes.com and saves the raw .html files to a directory.
The default is to scrape random pages from within a range of page numbers. To instead scrape a specific list of pages, replace rand_choice variable with an array of selected page numbers.

Instructions: add directory paths you would like to save the raw .html files and pages tried log in USER INPUT. In USER INPUT you can also select a range of page numbers to choose randomly, or replace rand_choice with an array of page numbers you would like to scrape. Also specify the number of cores you would like to run the scraping function with, as this code runs the scraper loop in parallel to increase speed.

Code by Kaelynn Rose (c)
Created on 2/22/2021

'''

import numpy as np
import numpy.random as random
import requests
import json
from bs4 import BeautifulSoup
from joblib import Parallel,delayed


################## USER INPUT ###################

html_path = '/Users/kaelynnrose/Documents/GALVANIZE/Capstones/Capstone_1/raw_html/' # path to directory you would like to store the .html files in
log_path = '/Users/kaelynnrose/Documents/GALVANIZE/Capstones/Capstone_1/logs/' # path to directory where you would like to store the log of pages tried

num_array = np.arange(6663,283432) # choose page range to request. pages outside of this range are blank.
rand_choice = random.choice(num_array,size=len(num_array),replace=False) # randomly sample page numbers

cores = 4 # select number of cores on your machine you would like to use to run the scraper in parallel

################## END USER INPUT ###############


pages_tried = [] # initialize list of pages tried in case an error stops the scraper
np.save(log_path + 'masterlog.npy',pages_tried) # save a master log of the pages already tried

def scrape_webpage(i):
    if i not in pages_tried:
        try:
            print('Working on page number ' + str(i))
            url = 'https://www.allrecipes.com/recipe/' + str(i)
            result = requests.get(url)
            soup = BeautifulSoup(result.content,'html.parser')
            text1 = str(soup.find_all('script',type='application/ld+json')[0]) # test to see whether the 'script' tag exists, if it does not this will go to the 'except' statement and then try the next page
            text_r1 = text1.split('<script type="application/ld+json">')[1].split('</script>')[0]
            pages = list(np.load(log_path+'masterlog.npy',allow_pickle=True))
            pages.append(i)
            np.save(dirpath+'masterlog.npy',pages) # add the page tried to the master log of pages_tried
            with open(html_path+'page'+str(i)+'.html', "w") as file:
                file.write(str(soup)) # write the file
        except:
            print(f'Recipe # {i} does not exist. No data obtained for this recipe.')
            try:
                errors = list(np.load(log_path+'masterlog.npy',allow_pickle=True))
                errors.append(i)
                np.save(log_path+'masterlog.npy',errors) # add the page tried to the master log of pages_tried
            except:
                print('Pickle error. Page will not be logged in pages_tried. Moving to next page.')

Parallel(n_jobs=cores)(delayed(scrape_webpage)(i) for i in rand_choice) # run scrape_webpage loop in parallel on 4 cores for each value of rand_choice




