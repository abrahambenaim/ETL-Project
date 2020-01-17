#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
import numpy as np
import requests
import json
import pprint as pp

# Yelp API Key
gkey = 'fxuoEjmZHd5kA1x20u4z2waSsXfTm49pWr2F6ac-htERJ0haCqXH949tlmDYt9lhy4MC6nBJjt2llMwhQJfxbwX69QlFkI221WkMDZTn7NMQBaXRrWGBFzCrg4-9XXYx'


# In[2]:


from etl_clean_ip import zip_list


# In[3]:


#set up base url
# base url
base_url = "https://api.yelp.com/v3/businesses/search"

# set up api_key dictionary
headers = {
        'Authorization': 'Bearer %s' % gkey,
    }

# set up a parameters dictionary
def s_params(target_loc,target_key,target_type):
    params = {
    "location": target_loc,
    "term": target_key,
    "categories": target_type,
}
    return params

# run a request using our params dictionary
def s_query(base_url,headers,params):
    response = requests.request('GET', base_url, headers=headers, params=params).json()
    return response


# In[4]:


# Import zip list
zip_list 


#cities_pd.shape[0] #use .shape[0] to count the number of rows


# In[3]:


# create empty lists to hold yelp data
id=[]
names = []
streets = []
zipcodes= []
cities = []
states = []
ratings = []
price = []

#define Yelp function to get restaurant data
def get_restaurants(loc):
    
    #these are the additional params
    add_params = { "limit" : 50, "sort_by": "best_match"}

    #these are the original params
    params = s_params(loc,"restaurants","restaurants, All")

    #add additional params to our params from before
    s1_params = {**params,**add_params}

    s1_results = s_query(base_url,headers,s1_params)

    res=0
    results=[]
    
##loop through values in s1_results dict;key= ['businesses'] value= list_info
    print(len(s1_results['businesses']))
    for list_info in s1_results['businesses']:
        try:
            id=list_info["id"]
            name=list_info["name"]
            address1 = list_info["location"]["address1"]
            city = list_info["location"]["city"]
            state = list_info["location"]["state"]
            zipcode = list_info["location"]["zip_code"]
            rating = list_info["rating"]
            price = list_info["price"]
            output = [name,address1,city,state,zipcode,rating,price,id] 
            results.append(output)
            print(output)
        except:
            print(f'Key not found. Missing data.')
            continue

    return results


# In[6]:


# Loop through the zipcodes in zip_list and append restaurant info to lists above
print("Beginning Data Retrieval")
print("-----------------------------------")

# restaurants = []

for zipc in zip_list:
    loc = zipc
    results = get_restaurants(loc)

    for output in results:
        id.append(output[7])
        names.append(output[0])
        streets.append(output[1])
        cities.append(output[2])
        states.append(output[3])
        zipcodes.append(output[4])
        ratings.append(output[5])
        price.append(output[6])

print("-----------------------------------")
print("Data Retrieval Complete")

    
print("done!")


# In[7]:


# Add columns for lat, lng, airport name, airport address, airport rating
restaurants_df = pd.DataFrame({"ID": id, "Name": names,"Location": streets, "City": cities, "State": states, "Zipcode":zipcodes, "Rating": ratings,"Price": price})
restaurants_df = restaurants_df.sort_values(by=["ID"])
restaurants_clean = restaurants_df.drop_duplicates(subset="ID", keep="first")
restaurants_clean.sort_values(by=["Zipcode"])


# In[8]:


len(restaurants_df['Zipcode'])/len(set(restaurants_df['Zipcode']))


# In[ ]:





# In[9]:


# Save Data to csv

# Visualize to confirm airport data appears


# In[ ]:




