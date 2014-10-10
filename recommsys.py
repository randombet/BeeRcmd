# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 16:11:06 2014
Building a Beer Recommendation System in Python
@author: Yixuan
"""
import pandas.io.sql as psql
import MySQLdb
import pandas as pd
import numpy as np
import math
#import scipy as sc
#import costFun

mysql_cn= MySQLdb.connect(host='localhost', 
                port=3306,user='root', passwd='*',#need to be filled 
                db='beer')
df= psql.read_sql('select distinct beer_name,review_overall, \
review_aroma,review_appearance,review_palate,review_taste,\
review_profilename from review_test;', con=mysql_cn) 


beer_1, beer_2 = "Amstel Light", "American Pale Ale"

beer_1_reviewers = df[df.beer_name==beer_1].review_profilename.unique()
beer_2_reviewers = df[df.beer_name==beer_2].review_profilename.unique()
common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers)

def get_beer_reviews(beer, common_users):
    mask = (df.review_profilename.isin(common_users)) & (df.beer_name==beer)
    reviews = df[mask].sort('review_profilename')
    reviews = reviews[reviews.review_profilename.duplicated()==False]
    return reviews
'''beer_1_reviews = get_beer_reviews(beer_1, common_reviewers)
beer_2_reviews = get_beer_reviews(beer_2, common_reviewers)'''

from scipy.stats.stats import pearsonr

ALL_FEATURES = ['review_overall', 'review_aroma', 'review_appearance','review_palate', 'review_taste']

def sim_person(p1,p2):
    #Get the list of mutually rated items
    p_1_beers = df[df.review_profilename==p1].beer_name.unique()
    p_2_beers = df[df.review_profilename==p2].beer_name.unique()
    common_beers = set(p_1_beers).intersection(p_2_beers)
    #if they are no rating in common, return 0
    n = len(common_beers)
    if n== 0:
        return 0
    #sum calculations
    mask = (df.beer_name.isin(common_beers)) & (df.review_profilename==p1)
    p_1_reviews=pd.DataFrame(df[mask],columns=ALL_FEATURES)
    mask = (df.beer_name.isin(common_beers)) & (df.review_profilename==p2)
    p_2_reviews=pd.DataFrame(df[mask],columns=ALL_FEATURES)
    s=np.size(p_1_reviews)
    y1=p_1_reviews.values.reshape((1,s))
    y2=p_2_reviews.values.reshape((1,s))
    return pearsonr(y1[0],y2[0])[0]



def calculate_similarity(beer1, beer2):
    # find common reviewers
    beer_1_reviewers = df[df.beer_name==beer1].review_profilename.unique()
    beer_2_reviewers = df[df.beer_name==beer2].review_profilename.unique()
    common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers)
    # get reviews
    beer_1_reviews = pd.DataFrame(get_beer_reviews(beer1, common_reviewers),columns=[ALL_FEATURES])
    beer_2_reviews = pd.DataFrame(get_beer_reviews(beer2, common_reviewers),columns=[ALL_FEATURES])
    corr = []
    s=len(common_reviewers)
    if s==0:
        return [0]*len(ALL_FEATURES)
    cursor = mysql_cn.cursor()
    for f in ALL_FEATURES:
        y1=beer_1_reviews[f].values.reshape((1,s))
        y2=beer_2_reviews[f].values.reshape((1,s))
        corr.append(pearsonr(y1[0],y2[0])[0])
    sim_overall=0 if math.isnan(corr[0]) else corr[0] 
    sim_aroma=0 if math.isnan(corr[1]) else corr[1]
    sim_appearance=0 if math.isnan(corr[2]) else corr[2]
    sim_palate=0 if math.isnan(corr[3]) else corr[3]
    sim_taste=0 if math.isnan(corr[4]) else corr[4]
    add_corr = ("INSERT INTO similar_beer(beer1,beer2,sim_overall,\
                sim_aroma,sim_appearance,sim_palate,sim_taste) \
              VALUES(%s, %s, %s,%s,%s,%s,%s)")
    data_corr =(beer1,beer2,sim_overall,\
              sim_aroma,sim_appearance,sim_palate,sim_taste)        
    cursor.execute(add_corr,data_corr)
    mysql_cn.commit()
    cursor.close()
    return corr

beers = df.beer_name.unique()

#similarity = []
def gen_sim_table():
    for beer1 in beers:
        try:
            print("starting", beer1)
        except:
            print('encoding error, passed')
        for beer2 in beers:
            if beer1 != beer2:
                calculate_similarity(beer1, beer2)

def rcmd(my_beer):
    num_item=3
    get_sim=('select distinct beer1,beer2,sim_overall,sim_aroma,sim_appearance,\
    sim_palate,sim_taste from similar_beer where beer1=\'%s\';' %my_beer)
    simdb=psql.read_sql(get_sim,con=mysql_cn).sort('sim_overall')
    mask_top=simdb.sim_overall>0 
    mask_tail=simdb.sim_overall<0
    top_rcmd=list(simdb[mask_top].beer2.tail(num_item))
    end_avd=list(simdb[mask_tail].beer2.head(num_item))
    try:
        print('Recommended beers:',top_rcmd)
        print('Try to avoid:',end_avd)
    except:
        pass
    return {'recommand':top_rcmd,'avoiding':end_avd}
    


#cols = ["beer1", "beer2", "overall_sim", "aroma_sim",'appearance_sim', "palate_sim", "taste_sim"]
#similarity = pd.DataFrame(similarity, columns=cols)
#print(similarity.tail())


#Allow the User to Customize the Weights

'''def calc_distance(dists, beer1, beer2, weights):
    mask = (dists.beer1==beer1) & (dists.beer2==beer2)
    row = dists[mask]
    row = row[['overall_dist', 'aroma_dist', 'palate_dist', 'taste_dist']]
    dist = weights * row
    return dist.sum(axis=1).tolist()[0]

weights = [2, 1, 1, 1]
print(calc_distance(simple_distances, "Amstel Light",\
"Caldera Ginger Beer", weights))
print(calc_distance(simple_distances,"Vas Deferens Ale","Caldera IPA"\
, weights))

#Find Similar Beers for Coors Light
my_beer = "Old Growth Imperial Stout"
results = []
for b in beers:
    if my_beer!=b:
        results.append((my_beer, b, calc_distance(simple_distances, my_beer, b, weights)))
for i in sorted(results, key=lambda x: x[2]):
    print(i);'''
mysql_cn.close()