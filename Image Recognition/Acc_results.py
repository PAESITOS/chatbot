## --- COMPARING THE SERVICES --- ##
""" This script opens the file where the data is stored and show it 
    in form of graphs to get a conclusion of which service works best 
    in a quantitative way """

# -- IMPORTED LIBRARIES -- # 
import io
import os
import pickle
import csv

import matplotlib.pyplot as plt
import numpy as np

from operator import itemgetter
from collections import OrderedDict

# -- FUNCTION DEFINITIONS -- #

def get_data():
    """ 
    This function loads the data saved in the "pkl" file and returns it. 
    """
    file = open('results.pkl','rb')
    file_wgo = open('google_words.pkl','rb')
    file_wam = open('amazon_words.pkl','rb')
    return pickle.load(file), pickle.load(file_wgo), pickle.load(file_wam)

def showing_data(results,wgoogle,wamazon):
    """
    This function reorganizes the data and plots the graphs  
    """
    # -- PLOTTING POSITION -- #
    fig1 = plt.figure(figsize=(12,8))
    plt.hist((results['pos_google'],results['pos_amazon']),bins=np.arange(13)-0.5,\
            label=("Google Positions","Amazon Positions"),density=False,alpha=1,color=('royalblue','darkorange'))
    plt.title("Histogram of the Frequency based on Positions ")
    plt.xlabel("Positions")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.xticks(range(12))
    plt.axis([0.25, 11.75,0,170])
    plt.savefig('Out/Positions.png',bbox_inches='tight')
    plt.close(fig1)

    # -- SCORE OF THE FIRST POSITION -- #
    samples = len(results['file_name'])
    ind_google = [i for i in range(samples) if results['pos_google'][i] == 1]
    ind_amazon = [i for i in range(samples) if results['pos_amazon'][i] == 1]
    scr_google =[ results['score_google'][i] for i in ind_google]
    scr_amazon =[ results['score_amazon'][i] for i in ind_amazon]
    spl_google = len(scr_google)
    spl_amazon = len(scr_amazon)

    # -- SCORE OF THE DETECTED POSITIONS -- #
    indten_google = [i for i in range(samples) if results['pos_google'][i] <= 10]
    indten_amazon = [i for i in range(samples) if results['pos_amazon'][i] <= 10]
    scrten_google =[ results['score_google'][i] for i in indten_google]
    scrten_amazon =[ results['score_amazon'][i] for i in indten_amazon]
    splten_google = len(scrten_google)
    splten_amazon = len(scrten_amazon)
    avgten_scr_google = sum(scrten_google)/float(splten_google)
    avgten_scr_amazon = sum(scrten_amazon)/float(splten_amazon)
    fig2 = plt.figure(figsize=(12,8))
    plt.plot(range(splten_google),scrten_google,'-',linewidth=0.9,label='Google Score',color='royalblue')
    plt.axhline(y=avgten_scr_google,xmin=0,xmax=splten_google,linewidth=2,\
                label='Average Google Score',color='navy',alpha=1)
    plt.plot(range(splten_amazon),scrten_amazon,'-',linewidth=0.9,label='Amazon Score',color='darkorange')
    plt.axhline(y=avgten_scr_amazon,xmin=0,xmax=spl_amazon,linewidth=2,\
                label='Average Amazon Score',color='orangered',alpha=1)
    plt.title('Score of the Detected Positions')
    plt.xlabel('Requests')
    plt.ylabel('Score')
    plt.legend(loc='lower left')
    plt.grid(True)
    plt.axis([0,max(splten_google,splten_amazon),0.0,1])
    plt.savefig('Out/Detected_Score.png',bbox_inches='tight')
    plt.close(fig2)

    # -- MOST COMMON GOOGLE WORDS -- #
    wgoo_sort = OrderedDict(sorted(wgoogle.items(), key=itemgetter(1),reverse=True))
    lvgoogle = []
    lkgoogle = []
    keys = wgoo_sort.keys()
    for key in keys:
        if wgoo_sort[key] >= 15:
            lkgoogle.append(key)
            lvgoogle.append(wgoo_sort[key])
    fig3 = plt.figure(figsize=(12,8))
    plt.bar(range(len(lkgoogle)),lvgoogle,color='royalblue')
    plt.title('Most Common Labels in Google Image Vision')
    plt.xlabel('Labels')
    plt.ylabel('Frequency')
    plt.xticks(range(len(lkgoogle)),lkgoogle,rotation=90)
    plt.savefig('Out/Google_Labels.png',bbox_inches='tight')
    plt.close(fig3)

    # -- MOST COMMON AMAZON WORDS -- #
    wama_sort = OrderedDict(sorted(wamazon.items(), key=itemgetter(1),reverse=True))
    lvamazon = []
    lkamazon = []
    keys = wama_sort.keys()
    for key in keys:
        if wama_sort[key] >= 15:
            lkamazon.append(key)
            lvamazon.append(wama_sort[key])
    fig4 = plt.figure(figsize=(12,8))
    plt.bar(range(len(lkamazon)),lvamazon,color='darkorange')
    plt.title('Most Common Labels in Amazon Rekognition')
    plt.xlabel('Labels')
    plt.ylabel('Frequency')
    plt.xticks(range(len(lkamazon)),lkamazon,rotation=90)
    plt.savefig('Out/Amazon_Labels.png',bbox_inches='tight')
    plt.close(fig4)

    # -- PRINTING PUNTUATION -- #
    with open('Out/Results.txt','w') as text_file:
        text_file.write('_-_-_-_-_-_-_-_-_-_-_-_-_ ACCURACY RESULTS _-_-_-_-_-_-_-_-_-_-_-_-_\n')
        text_file.write('(1) General Data:'+'\n')
        text_file.write('-- Total Requests: {}.\n'.format(samples))
        text_file.write('-- Google Detections: {}.\n'.format(splten_google))
        text_file.write('-- Amazon Detections: {}.\n'.format(splten_amazon))
        text_file.write('-- Google Detections Percentatge: {0:.2f}%.\n'.format((splten_google/samples)*100))
        text_file.write('-- Amazon Detections Percentatge: {0:.2f}%.\n'.format((splten_amazon/samples)*100))
        msg = (sum(results['score_google'])/float(samples))*100
        text_file.write('(2) Total Accuracy:\n')
        text_file.write('-- Total Google Accuracy: {0:.2f}%.\n'.format(msg))
        msg = (sum(results['score_amazon'])/float(samples))*100
        text_file.write('-- Total Amazon Accuracy: {0:.2f}%.\n'.format(msg))
        text_file.write('(3) Accuracy of the first Positions:\n')
        text_file.write('-- Google First Positions: {}.\n'.format(spl_google))
        text_file.write('-- Google First Detections Percentatge: {0:.2f}%.\n'.format((spl_google/samples)*100))
        text_file.write('-- Amazon First Positions: {}.\n'.format(spl_amazon))
        text_file.write('-- Amazon First Detections Percentatge: {0:.2f}%.\n'.format((spl_amazon/samples)*100))
        text_file.write('(4) Accuracy of the detected requests:\n')
        text_file.write('-- Detected Google Accuracy: {0:.2f}%.\n'.format(avgten_scr_google*100))
        text_file.write('-- Detected Amazon Accuracy: {0:.2f}%.\n'.format(avgten_scr_amazon*100))
    text_file.close()

def write_csv(results):
    """
    This function writes the dictionary results in a csv file.
    """
    punt_google = ['punt_google',results['punt_google']]
    punt_amazon = ['punt_amazon',results['punt_amazon']]
    results.pop('punt_google',None)
    results.pop('punt_amazon',None)
    keys = sorted(results.keys())
    with open('Out/Results.csv','w') as csv_file:
        writer = csv.writer(csv_file,delimiter = ",")
        writer.writerow(punt_google)
        writer.writerow(punt_amazon)
        writer.writerow(keys)
        writer.writerows(zip(*[results[key] for key in keys]))

def main():
    """ 
    This main program gets the results from a pickle file, and shows the
    data in form of graphs. Also the results obtained are writen in a csv file
    if the user wants to get more detailed results.
    """ 
    # -- GET THE RESULTS FROM A PICKLE FILE -- #
    results,wgoogle,wamazon = get_data()

    # -- PLOTTING THE RESULTS OBTAINED -- #
    showing_data(results,wgoogle,wamazon)

    # -- WRITING THE RESULTS IN A CSV FILE -- #
    write_csv(results)

if __name__ == '__main__':
    main()
