#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import pandas as pd


# In[3]:


file1 = "./MDC_Housing_Data.csv"
housing_data = pd.read_csv(file1)


# In[4]:


file2 = "./ZIP_TRACT_2019.csv"
zip_vs_tract = pd.read_csv(file2)


# In[5]:


file3 = './ACSST5Y2018.S1902_data_with_overlays_2020-01-11T105425.csv'
income_data = pd.read_csv(file3)


# In[6]:


housing_data
cols = [0,3,49]
housing_data = housing_data
housing_data = pd.DataFrame(housing_data.iloc[:, cols])


# In[7]:


new = housing_data.drop(housing_data.index[[0,2]])
new


# In[8]:


new_header = new.iloc[0] 
new = new[1:]
new.columns = new_header 


# In[9]:


new.head(25)
col_names = ['zip_code','home_value','rent_value']


# In[10]:


new.columns = col_names


# In[11]:


home_value_byzip = new
home_value_byzip


# In[12]:


zip_vs_tract = zip_vs_tract[['zip','tract']]

zip_vs_tract


# In[13]:


zip_data = new.join(zip_vs_tract)
zip_data = zip_data[['zip_code','home_value','rent_value']]
zip_data['zip_code'] = zip_data.zip_code.astype(float)


# In[14]:


zip_data


# In[15]:


income_data = income_data[['GEO_ID','S1902_C03_001E']]

income_data


# In[16]:


income_data = income_data.drop(0)


# In[17]:


# new data frame with split value columns 
new = income_data["GEO_ID"].str.split("US", n = 1, expand = True) 
  
# making separate first name column from new data frame 
income_data["x"]= new[0] 
  
# making separate last name column from new data frame 
income_data["Tract"]= new[1] 


# In[18]:


income_data = income_data[['S1902_C03_001E','Tract']].rename(columns={'S1902_C03_001E':'Avg_income'})
income_data
income_data['Tract']=income_data['Tract'].astype(int)


# In[19]:


#income_data = pd.merge(left = income_data,right = zip_vs_tract, left_on='Tract', right_on='tract')
merged_left = pd.merge(left=income_data,right=zip_vs_tract, how='left', left_on='Tract', right_on='tract')


# In[20]:


merged_left = merged_left[['Avg_income','zip']]


# In[21]:


merged_left


# In[22]:


merged_left.dropna()
merged_left.Avg_income = pd.to_numeric(merged_left.Avg_income, errors='coerce').fillna(0).astype(int)


# In[23]:


merged_left


# In[24]:


avgincome_perzip = merged_left.groupby(['zip']).mean()


# In[25]:


avgincome_perzip


# In[26]:


#income_homevalue = pd.merge(left=zip_data,right=merged_left, how='inner', left_on='zip_code', right_on='zip')
income_homevalue = pd.merge(left=avgincome_perzip,right=zip_data, how='inner', left_on='zip', right_on='zip_code')


# In[27]:


income_homevalue['rule_of_thumb'] = (income_homevalue.Avg_income * 0.3 / 12).round(3)


# In[28]:


income_homevalue['rent_value'] = income_homevalue['rent_value'].str.replace('$','').str.replace(',','')
income_homevalue['rent_value'] = pd.to_numeric(income_homevalue.rent_value, errors='coerce').fillna(0).astype(int)


# In[29]:


income_homevalue['home_value'] = income_homevalue['home_value'].str.replace('$','').str.replace(',','')
income_homevalue['home_value'] = pd.to_numeric(income_homevalue.home_value, errors='coerce').fillna(0).astype(int)


# In[30]:


income_homevalue['disparity'] = income_homevalue.rent_value - income_homevalue.rule_of_thumb


# In[31]:


income_homevalue = income_homevalue.sort_values(by='disparity', ascending= False).sort_values(by='Avg_income')


# In[32]:


income_homevalue = income_homevalue[income_homevalue.rent_value != 0]


# In[33]:


top30_disparity = income_homevalue.head(30)


# In[34]:


top30_disparity['zip_code'] = top30_disparity['zip_code'].astype(int)
top30_disparity['Avg_income'] = top30_disparity['Avg_income'].round(3)


# In[35]:


top30_disparity = top30_disparity.reset_index(drop=True)


# In[36]:


zip_list = top30_disparity['zip_code'].tolist()


# In[37]:


zip_list


# In[ ]:




