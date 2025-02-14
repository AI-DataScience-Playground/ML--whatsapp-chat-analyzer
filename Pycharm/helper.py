from urlextract import URLExtract

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


def get_words_count(df):
    words = []
    for message in df['messages']:
        words.extend(message.split())

    return len(words)