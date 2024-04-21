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
```
api_service_name = "youtube"
api_version = "v3"
api_key='AIzaSyB6cmqZxAgsDC4mCgfpyL6IChq_AOzvU-c'
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
```
Fetch channel info 
```
def channel_info(channel_id): 
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id)
    response = request.execute()

    if 'items' not in response or len(response['items']) == 0:
        st.error("No channel found with the provided ID.")
        return

    channel_data = response['items'][0]
    data = [{
        'channel_name': channel_data['snippet']['title'],
        'channel_des': channel_data['snippet']['description'],
        'channel_uploadId': channel_data['contentDetails']['relatedPlaylists']['uploads'],
        'channel_sub': channel_data['statistics']['subscriberCount'],
        'channel_vedioCount': channel_data['statistics']['videoCount'],
        'channel_viewCount': channel_data['statistics']['viewCount']
    }]
    st.write(pd.DataFrame(data))
    
    # here going to insert data into my sql channel table

    query = '''INSERT INTO project.channel (channel_name,channel_des,channel_uploadId,channel_sub,channel_vedioCount,
            channel_viewCount) VALUES (%s, %s, %s,%s,%s,%s)'''
    
    mycursor.execute(query,(data[0]['channel_name'],
                            data[0]['channel_des'],
                            data[0]['channel_uploadId'],
                            data[0]['channel_sub'],
                            data[0]['channel_vedioCount'],
                            data[0]['channel_viewCount']))
    mydb.commit()
```
https://github.com/PraveenkuamrA/YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit/blob/3af67bd3bba565cf0bfd55e7222b54a8548c915b/YouTube%20Data%20Harvesting%20and%20Warehousing%20using%20SQL%20and%20Streamlit.py#L20-L50

