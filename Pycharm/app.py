import streamlit as st
import preprocessor
import helper

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    users_list = df['users'].unique().tolist()
    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", users_list)

    if(st.sidebar.button('Analyze')):
        st.dataframe(df[(df['users'] == selected_user) | (selected_user == 'Overall')])

        message_count, words_count, media_count, urls_count = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4, gap="large")

        with col1:
            st.header('Msg Count')
            st.title(message_count)

        with col2:
            st.header('Words Count')
            st.title(words_count)

        with col3:
            st.header('Media Count')
            st.title(media_count)

        with col4:
            st.header('URL Count')
            st.title(urls_count)