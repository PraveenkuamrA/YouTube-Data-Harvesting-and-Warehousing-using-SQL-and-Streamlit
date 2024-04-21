import streamlit as st
import googleapiclient.discovery
import pandas as pd
import mysql.connector
import time

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 )
mycursor = mydb.cursor(buffered=True)

api_service_name = "youtube"
api_version = "v3"
api_key='AIzaSyB6cmqZxAgsDC4mCgfpyL6IChq_AOzvU-c'
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


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

    query = '''INSERT INTO project.channel (channel_name,channel_des,channel_uploadId,channel_sub,channel_vedioCount,
            channel_viewCount) VALUES (%s, %s, %s,%s,%s,%s)'''
    
    mycursor.execute(query,(data[0]['channel_name'],
                            data[0]['channel_des'],
                            data[0]['channel_uploadId'],
                            data[0]['channel_sub'],
                            data[0]['channel_vedioCount'],
                            data[0]['channel_viewCount']))
    mydb.commit()

def playlist_details(channel_id):
    play_info=[]
    next_page_token=None
    while True:
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id)
        response = request.execute()

        if 'items' not in response or len(response['items']) == 0:
            st.error("No playlist found with the provided channel ID!!!...")
            return
 
        channel = response['items'][0]
        channel_name=channel['snippet']['title']
        channel_ids=channel['contentDetails']['relatedPlaylists']['uploads']
        request = youtube.playlists().list(part='snippet,contentDetails',channelId=channel_id,maxResults=50,pageToken=next_page_token)
        response1 = request.execute()

        for item in response1['items']: 
            data=[{
                'playList_Id' : item['id'],
                'playList_Title' : item['snippet']['title'], 
                'vedio_count' : item['contentDetails']['itemCount']
            }]
            query = '''INSERT INTO project.playlist (channel_name,channel_ids,playList_Id,playList_Title,
                        vedio_count) VALUES (%s, %s, %s,%s,%s)'''
    
            mycursor.execute(query,(channel_name,
                                    channel_ids,
                                    data[0]['playList_Id'],
                                    data[0]['playList_Title'],
                                    data[0]['vedio_count']))
        
            play_info.append(*(data))
        
        if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
        else:
            break
    mydb.commit()
    st.write(pd.DataFrame(play_info))

def vedioIds_info(channel_id): 

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_ids)
    response = request.execute()

    if 'items' not in response or len(response['items']) == 0:
        st.error("No vedio Ids  found with the provided channel ID!!!...")
        return
    
    channeldata=response['items'][0]

    PLAYLIST_ID=channeldata['contentDetails']['relatedPlaylists']['uploads']
    channel_name=channeldata['snippet']['title']

    video_ids=[]
    next_page_token=None
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=PLAYLIST_ID,
            maxResults=50,
            pageToken=next_page_token)
        
        response1 = request.execute()

        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        if 'nextPageToken' in response1: 
            next_page_token = response1.get('nextPageToken')
        else:
            break
    return video_ids,channel_name

def vedios_info(video_ids,channel_name):

    channel_Name=channel_name
    print(channel_Name)
    vedio_data=[]

    def time_str_to_seconds(t):
        def time_duration(t):
            a = pd.Timedelta(t)
            b = str(a).split()[-1]
            return b
        time_str = time_duration(t)
            
        hours, minutes, seconds = map(int, time_str.split(':'))
        total_seconds = (hours * 3600) + (minutes * 60) + seconds
            
        return total_seconds

    for item in video_ids:
        video_id = item
        video_request= youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id)
        response=video_request.execute()

        date=list(response['items'][0]['snippet']['publishedAt'].split('T'))
        data=[{  
                'channel_name' : channel_Name,
                'vedio_ID' : item ,
                'vedio_title' : response['items'][0]['snippet']['title'],
                'vedio_view' : response['items'][0]['statistics']['viewCount'],
                'vedio_date' : date[0],
                'vedio_duriation' :str(time_str_to_seconds(response['items'][0]['contentDetails']['duration'])),
                #Duration=str(time_str_to_seconds(item['contentDetails']['duration'])),
                'vedio_likes' : response['items'][0]['statistics']['likeCount'] 
                    if 'likeCount' in response['items'][0]['statistics'] else '0' ,
                'vedio_comment' : response['items'][0]['statistics']['commentCount']
                    if 'commentCount' in response['items'][0]['statistics'] else '0' ,
                'vedio_des' : response['items'][0]['snippet']['description']
            }]
        
        query='''insert into project.vedio(channel_name,vedio_ID,vedio_title,vedio_view,vedio_date,
                vedio_duriation,vedio_likes,vedio_comment,vedio_des) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        
        mycursor.execute(query,(channel_Name,item,
                                data[0]['vedio_title'],
                                data[0]['vedio_view'],
                                data[0]['vedio_date'],
                                data[0]['vedio_duriation'],
                                data[0]['vedio_likes'],
                                data[0]['vedio_comment'],
                                data[0]['vedio_des']))

        vedio_data.append(*(data))
    
    mydb.commit()
    st.write(pd.DataFrame(vedio_data))

def comment_info(video_ids,channel_name):
    comments_details=[]
    channel_Names=channel_name
    
    for item in video_ids:
        j=0
        next_page_token=None
        try:
            while(j<=1):
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=item,
                    maxResults=50,
                    pageToken=next_page_token)
                
                response = request.execute()
                for i in range(len(response['items'])):
                    data=[{
                        'channel_Name' : channel_Names,
                        'comment' : response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'],
                        'comment_author' : response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'comment_date' : response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'].split('T')[0],
                        'comment_vedioID' : response['items'][i]['snippet']['topLevelComment']['snippet']['videoId']
                    }]
                    query=('''insert into project.comments(channel_Name,vedio_comment,comment_author,comment_date,
                        comment_vedioID) values(%s,%s,%s,%s,%s)''')   
                    mycursor.execute(query,(data[0]['channel_Name'],data[0]['comment'],data[0]['comment_author'],
                                    data[0]['comment_date'],data[0]['comment_vedioID']))
                    comments_details.append(*(data))

                if 'nextPageToken' in response: 
                    next_page_token = response.get('nextPageToken')
                    j+=1
                else:
                    break
        except: 
            pass
    

    mydb.commit()  
    st.write(pd.DataFrame(comments_details))

 
channel_ids = st.text_input(':orange[CHANNEL ID]', 'Give input here ', key="unique_key_for_text_input")


with st.sidebar:
    st.title(":red[YOUTUBE DATA HARVESTING AND WAREHOUSING USING SQL AND STREAMLIT]")
    st.header("Problem Statement")
    st.caption(''':orange[The problem statement is to create a Streamlit application that allows users
                to access and analyze data from multiple YouTube channels.]''')
    st.header(":green[DATA TABLES]")

def CHANNEL():

    message="This is the updated channel data "
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.15)

    mycursor.execute('select * from project.channel')
    out=mycursor.fetchall()
    header=[i[0] for i in mycursor.description]
    yield pd.DataFrame(out,columns=header)


if st.sidebar.button("CHANNEL"):
    st.write(CHANNEL)

def PLAYLIST(): 
    message='This is the updated playlist data '
    for word in message.split(" "): 
        yield word + " "
        time.sleep(0.15)
    mycursor.execute('select * from project.playlist')
    out=mycursor.fetchall()
    header=[i[0] for i in mycursor.description]
    yield pd.DataFrame(out,columns=header)

if st.sidebar.button('PLAYLIST'): 
    st.write(PLAYLIST)

def VEDIO(): 
    message='This is the updated vedio data'
    for word in message.split(' '): 
        yield word + ' '
        time.sleep(0.15)
    mycursor.execute('select * from project.vedio')
    out=mycursor.fetchall()
    header=[i[0] for i in mycursor.description]
    yield pd.DataFrame(out,columns=header)

if st.sidebar.button('VEDIO'): 
    st.write(VEDIO)

def COMMENTS(): 
    message='This is the updated comments data'
    for word in message.split(' '): 
        yield word + ' '
        time.sleep(0.15)
    mycursor.execute('select * from project.comments')
    out=mycursor.fetchall()
    header=[i[0] for i in mycursor.description]
    yield pd.DataFrame(out,columns=header)

if st.sidebar.button('COMMENTS'): 
    st.write(COMMENTS)

questions=st.selectbox(":orange[SELECT QUESTION]",("select option",
        "1 . What are the names of all the videos and their corresponding channels?",
        "2 . Which channels have the most number of videos, and how many videos dothey have?",
        "3 . What are the top 10 most viewed videos and their respective channels?",
        "4 . How many comments were made on each video, and what are their corresponding video names?",
        "5 . Which videos have the highest number of likes, and what are their corresponding channel names?",
        "6 . What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
        "7 . What is the total number of views for each channel, and what are their corresponding channel names?",
        "8 . What are the names of all the channels that have published videos in the year 2022?",
        "9 . What is the average duration of all videos in each channel, and what are their corresponding channel names?",
        "10 . Which videos have the highest number of comments, and what are their corresponding channel names?"))

if questions=="1 . What are the names of all the videos and their corresponding channels?":
    
    mycursor.execute('select channel_name,vedio_title from project.vedio')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['channel_Name','vedio_Title']))

elif questions=="2 . Which channels have the most number of videos, and how many videos dothey have?": 
    
    mycursor.execute('''select channel_name,channel_vedioCount from project.channel 
                    order by channel_vedioCount desc''')
    data=mycursor.fetchall() 
    st.write(pd.DataFrame(data,columns=['Channel_Name','Vedio_Count']))

elif questions=="3 . What are the top 10 most viewed videos and their respective channels?": 
    
    mycursor.execute('''select channel_name,vedio_title,vedio_view from project.vedio
                 order by vedio_view desc 
                 limit 10 ''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['CHANNEL','VEDIO','VIEWS'],index=[1,2,3,4,5,6,7,8,9,10]))

elif questions=="4 . How many comments were made on each video, and what are their corresponding video names?": 
   
    mycursor.execute('''select vedio_title,vedio_comment,channel_name from project.vedio''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['VEDIO','COMMENT_COUNT','CHANNEL']))

elif questions=="5 . Which videos have the highest number of likes, and what are their corresponding channel names?": 
    
    mycursor.execute('''select channel_name,vedio_title,vedio_likes from project.vedio
                 order by vedio_likes desc''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['CHANNEL','VEDIO_TITLE','LIKES_COUNT']))

elif questions=="6 . What is the total number of likes and dislikes for each video, and what are their corresponding video names?": 

    mycursor.execute('''select vedio_title , vedio_likes from project.vedio ''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['VEDIO_TITLE','NO OF LIKES']))

elif questions=="7 . What is the total number of views for each channel, and what are their corresponding channel names?":

    mycursor.execute('''select channel_name , channel_viewCount from project.channel''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['CHANNEL NAME','VIEW COUNT']))

elif questions=="8 . What are the names of all the channels that have published videos in the year 2022?": 
    mycursor.execute('''select channel_name,vedio_title,vedio_date from project.vedio
                 where extract(year from vedio_date)=2022 ''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['CHANNEL NAME','VEDIO TITLE','VEDIO DATE']))

elif questions=="9 . What is the average duration of all videos in each channel, and what are their corresponding channel names?":

    mycursor.execute('''select channel_name,avg(vedio_duriation) from project.vedio
                 group by channel_name ''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['CHANNEL NAME','VEDIO DURIATION in seconds']))

elif questions== "10 . Which videos have the highest number of comments, and what are their corresponding channel names?":

    mycursor.execute('''select channel_name,vedio_title,vedio_comment from project.vedio
                 order by vedio_comment desc''')
    data=mycursor.fetchall()
    st.write(pd.DataFrame(data,columns=['CHANNEL NAME','VEDIO TITLE','COMMENT COUNT']))


channel_info(channel_ids)
playlist_details(channel_ids)
a=vedioIds_info(channel_ids)
vedios_info(a[0],a[1])
comment_info(a[0],a[1])
st.success('successfully inserted data into local host database!', icon="✅")


