import re
import pandas as pd
def preprocess(data):
    pattern='\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}\s-\s'    
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date':'date'},inplace=True)
    user=[]
    message=[]
    for m in df['user_message']:
        entry=re.split('([\w\W]+?):\s',m)
        if(len(entry)==1):
            user.append("Group Notification")
            message.append(entry[0].replace("\n",""))
        else:
            user.append(entry[1])
            message.append(entry[2].replace("\n",""))

    df['message']=message
    df['user']=user

    date=[]
    time=[]
    days=[]

    for i in df['date']:
        date.append('{}-{}-{}'.format(i.day,i.month,i.year))
        time.append('{}:{}'.format(i.hour,i.minute))
        days.append(i.day_name())

    df.drop(columns=['user_message'],inplace=True)
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day']=df['date'].dt.day
    df['month']=df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['year']=df['date'].dt.year
    

    df['date']=date
    df['time']=time
    df['days']=days
    period = []
    for hour in df[['days', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df