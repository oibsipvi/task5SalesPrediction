# -*- coding: utf-8 -*-
"""Sales Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OF_EiP4zb-5PfwjmS48bt-1Qq0Ebfogx

#Importing the dependencies
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

"""#Data collection and Analysis"""

#loading the dataset from CSV file to pandas dataframe
big_mart_data= pd.read_csv('/content/Big mart.csv')

#first 5 rows of dataframe
big_mart_data.head()

#Number of datapoint and number of Features
big_mart_data.shape

#Getting some information about the dataset
big_mart_data.info()

"""#Categorical Fearture: 
  Item_Identifier 
  Item_Fat_Content 
  Item_Type
  Outlet_Identifier
   Outlet_Size 
   Outlet_Location_Type
 Outlet_Type  
"""

#checking formissing values
big_mart_data.isnull().sum()

"""#Handling missing values

Mean --> average value

Mode --> Most repeated value
"""

#mean value of "Item_weight" column
big_mart_data['Item_Weight'].mean()

#Filling the missing value in "Item_Weight" column with mean value
big_mart_data['Item_Weight'].fillna(big_mart_data['Item_Weight'].mean(),inplace=True)

#checking for missing values
big_mart_data.isnull().sum()

"""replacing the missing values in "Outlet_Size" with mode"""

mode_of_outlet_size= big_mart_data.pivot_table(values='Outlet_Size', columns='Outlet_Type', aggfunc=((lambda x: x.mode()[0])))

print(mode_of_outlet_size)

missing_values = big_mart_data['Outlet_Size'].isnull()

print(missing_values)

big_mart_data.loc[missing_values, 'Outlet_Size']= big_mart_data.loc[missing_values,'Outlet_Type'].apply(lambda x:mode_of_outlet_size)

#checking for missing values
big_mart_data.isnull().sum()

"""#DATA ANALYSIS"""

#statistical measures about the data
big_mart_data.describe()

#Numerical Features
sns.set()

#Item_Weight distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Weight'])
plt.show()

#Item_Visibility distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Visibility'])
plt.show()

#Item_MRP distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_MRP'])
plt.show()

#Item_Outlet_Sales distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Outlet_Sales'])
plt.show()

#Outlet_Establishment_Year distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Outlet_Establishment_Year'])
plt.show()

"""Categorical Features"""

#Item_Fat_Content column
plt.figure(figsize=(6,6))
sns.countplot(big_mart_data,x='Item_Fat_Content')
plt.show()

#Item_Type  column
plt.figure(figsize=(30,6))
sns.countplot(big_mart_data,x='Item_Type')
plt.show()

#Outlet_Size column
#plt.figure(figsize=(6,6))
#sns.countplot(big_mart_data,x='Outlet_Size')
#plt.show()

"""#DATA PRE_PROCESSING"""

big_mart_data.head()

big_mart_data['Item_Fat_Content'].value_counts()

big_mart_data.replace({'Item_Fat_Content':{'Low Fat':'Low Fat','LF':'Low Fat','reg':'Regular'}}, inplace=True)

big_mart_data['Item_Fat_Content'].value_counts()

"""Label Encoding"""

encoder= LabelEncoder()

big_mart_data['Item_Identifier']= encoder.fit_transform(big_mart_data['Item_Identifier'])

big_mart_data['Item_Fat_Content']= encoder.fit_transform(big_mart_data['Item_Fat_Content'])

big_mart_data['Item_Type']= encoder.fit_transform(big_mart_data['Item_Type'])

big_mart_data['Outlet_Identifier']= encoder.fit_transform(big_mart_data['Outlet_Identifier'])

#big_mart_data['Outlet_Size']= encoder.fit_transform(big_mart_data['Outlet_Size'])

big_mart_data['Outlet_Location_Type']= encoder.fit_transform(big_mart_data['Outlet_Location_Type'])

big_mart_data['Outlet_Type']= encoder.fit_transform(big_mart_data['Outlet_Type'])

"""#Splitting Features and target"""

x= big_mart_data.drop(columns='Item_Outlet_Sales', axis=1)
y= big_mart_data['Item_Outlet_Sales']

print(x)

print(y)

"""#Splitting the data into training and test data"""

x_train, x_test, y_train, y_test= train_test_split(x,y, test_size=0.2, random_state=2)

print(x.shape, x_train.shape, x_test.shape)

"""#Machine learning Model training: XGBRegressor"""

regressor= XGBRegressor()

regressor.fit(x_train,y_train)

"""#Evaluation"""

#prediction on training data
training_data_prediction= regressor.predict(x_train)

#R Square Error
r2_train= metrics.r2_score(y_train,training_data_prediction)

print('R Square Value: ',r2_train)

#prediction on test data
test_data_prediction= regressor.predict(x_test)

#R Square Error
r2_test= metrics.r2_score(y_test,test_data_prediction)