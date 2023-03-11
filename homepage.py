import streamlit as st
import pandas as pd
from wordcloud import WordCloud as wcl
import helper
import emoji
import preprocessor
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

def showemojistats(word_list):
    st.title("Emoji analysis")
    col1,col2=st.columns(2)
    emojis=[]
    for i in word_list.split(" "):
        p=[]
        for c in i:
            if emoji.is_emoji(c):
                p.append(c)
        emojis.extend(p)

    k=pd.DataFrame(Counter(emojis).most_common(10))
    k=k.rename(columns={0:'Most used Phrases',1:'Count'})
    with col1:    
        st.dataframe(k)
    with col2:
        fig,ax=plt.subplots()
        ax.bar(k['Most used Phrases'],k['Count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

def showwordstats(word_list):
    st.title("Word analysis")
    col1,col2=st.columns(2)
    p=word_list.split(" ")
    for i in p:
        for c in i:
            if emoji.is_emoji(c):
                p.remove(i)
                break

    k=pd.DataFrame(Counter(p).most_common(20))
    k=k.rename(columns={0:'Most used Phrases',1:'Count'})
    with col1:    
        st.dataframe(k)
    with col2:
        fig,ax=plt.subplots()
        ax.bar(k['Most used Phrases'],k['Count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)





def wordartcreate(selected,df):
    word_list,new_df=helper.fetch_wordart(df,selected)
    st.title('Word Analyzer')
    wl = wcl(background_color='white', width=1500, height=1500)
    wordart = wl.generate(word_list)
    fig, ax = plt.subplots()
    ax = plt.imshow(wordart)
    plt.axis("off")
    st.pyplot(fig)

    st.title("Message Frame")
    st.dataframe(new_df)

    showwordstats(word_list)
    showemojistats(word_list)
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    st.title('Activity Map')
    col1,col2 = st.columns(2)
    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)


def statshow(selected,df):
    num_messages, num_words= helper.fetch_stats(df, selected)
    #print(word_list)
    col1, col2 = st.columns(2)

    with col1:
        st.header("Total Messages")
        st.title(num_messages)

    with col2:
        st.header("Total words")
        st.title(num_words)

    if(selected == 'Overall'):
        st.header("Top Users Analyzer")
        col1,col2=st.columns(2)


        with col1:
            p = df['user'].value_counts().head()
            fig, ax = plt.subplots()
            ax.bar(p.index, p.values,)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(round(df['user'].value_counts()*100/df.shape[0],2).reset_index().rename(columns={'index':'name','user':'percent_active'}),use_container_width=True)

    wordartcreate(selected,df)



st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if(uploaded_file is not None):
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    #st.dataframe(df)

    #fetch unique users
    user=[]
    user=df['user'].unique().tolist()
    user.remove("Group Notification")
    user.sort()
    user.insert(0,"Overall")

    selected=st.sidebar.selectbox("Show userList",user)
    statshow(selected,df)

    st.sidebar.text("Follow us on Github")