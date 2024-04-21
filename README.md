# YouTube Data Harvesting and Warehousing using SQL and Streamlit 

## The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
 #### 1 . Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
 #### 2 . Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
 #### 3 . Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

Install google api connector 
 ```
pip install google-api-python-client
```
Install my Sql connector 
```
pip install mysql-connector_python
```
Install Streamlit 
```
pip install streamlit
```
Install pandas
```
pip install pandas
```
Import all functions
```
import streamlit as st
import googleapiclient.discovery
import pandas as pd
import mysql.connector
import time
```
Connect local host sql with compiler
```
mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 )
mycursor = mydb.cursor(buffered=True)
```
Connection with youtube api server with your api key

https://github.com/PraveenkuamrA/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/blob/3af67bd3bba565cf0bfd55e7222b54a8548c915b/YouTube%20Data%20Harvesting%20and%20Warehousing%20using%20SQL%20and%20Streamlit.py#L7-L12

Fetch channel info 

https://github.com/PraveenkuamrA/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/blob/3af67bd3bba565cf0bfd55e7222b54a8548c915b/YouTube%20Data%20Harvesting%20and%20Warehousing%20using%20SQL%20and%20Streamlit.py#L20-L50

