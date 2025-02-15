import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)

    df = pd.DataFrame({'date': date, 'message': messages})
    df['date'] = pd.to_datetime(df['date'].str.replace(' - ', ''), format='%d/%m/%Y, %I:%M %p')

    users = []
    messages = []
    for message in df['message']:
        entry = re.split(r'^(.*?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month

    return df