def refiner(df,selected_user):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]
    elif (selected_user == 'Overall'):
        df = df[df['user'] != 'Group Notification']

    new_df = df[df['message'] != "<Media omitted>"]


    new_df = new_df[df['message'] != "This message was deleted"]

    return new_df

    

def fetch_stats(df,selected_user):
    new_df=refiner(df,selected_user)
    t = []
    for i in new_df['message']:
        t.extend(i.split())

    return new_df.shape[0], len(t)




def fetch_wordart(df,selected_user):
    new_df=refiner(df,selected_user)
    art = new_df['message'].str.cat(sep=" ")
    

    return art,new_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['days'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='days', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
