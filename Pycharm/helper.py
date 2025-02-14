import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter

def fetch_stats(user, df):
    if user != 'Overall':
        df = df[df['users'] == user]

    message_count = df.shape[0]
    words_count = get_words_count(df)
    media_count = df[df['messages'] == '<Media omitted>\n'].shape[0]

    extractor = URLExtract()
    urls = []
    for message in df['messages']:
        urls.extend(extractor.find_urls(message))

    urls_count = len(urls)

    return message_count, words_count, media_count, urls_count


def fetch_most_active_users(df):
    x = df['users'].value_counts().head()
    percent_df = round(df['users'].value_counts() * 100 / df.shape[0], 2).reset_index().rename(columns={'users': 'name', 'count': 'percent'})
    return x, percent_df


def create_word_cloud(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['users'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user, df):
    stopwords = open('stop_hinglish.txt', 'r')
    stopwords = stopwords.read()

    if (selected_user != 'Overall'):
        df = df[df['users'] == selected_user]

    temp_df = df[(df['users'] != 'group_notification')]
    temp_df = temp_df[(temp_df['messages'].str.strip() != "<Media omitted>")]
    temp_df = temp_df[(temp_df['messages'].str.strip() != 'This message was deleted')]
    temp_df = temp_df[(temp_df['messages'].str.strip() != 'You deleted this message')]

    words = []
    for message in temp_df['messages']:
        for word in message.split():
            if word not in stopwords:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def get_words_count(df):
    words = []
    for message in df['messages']:
        words.extend(message.split())

    return len(words)