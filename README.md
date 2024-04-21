# YouTube Data Harvesting and Warehousing using SQL and Streamlit 

## The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
 #### 1 . Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
 #### 2 . Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
 #### 3 . Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

'''
import streamlit as st
import googleapiclient.discovery
import pandas as pd
import mysql.connector
import time
'''
