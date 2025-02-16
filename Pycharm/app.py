import streamlit as st
import preprocessor
import helper
import  matplotlib.pyplot as plt



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
            st.subheader('Msg Count')
            st.subheader(message_count)

        with col2:
            st.subheader('Words Count')
            st.subheader(words_count)

        with col3:
            st.subheader('Media Count')
            st.subheader(media_count)

        with col4:
            st.subheader('URL Count')
            st.subheader(urls_count)


        timeline = helper.get_monthly_timeline(selected_user, df)
        st.title('Monthly Stats')
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        timeline = helper.get_daily_timeline(selected_user, df)
        st.title('Daily Stats')
        fig, ax = plt.subplots()
        ax.plot(timeline['only_date'], timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.columns(2, gap='large')

        with col1:
            weekly_activity_df = helper.get_weekly_activity_map(selected_user, df)
            st.subheader('Most busy day')
            fig, ax = plt.subplots()
            ax.bar(weekly_activity_df['day_name'], weekly_activity_df['count'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            monthly_activity_map = helper.get_monthly_activity_map(selected_user, df)
            st.subheader('Most busy month')
            fig, ax = plt.subplots()
            ax.bar(monthly_activity_map.index, monthly_activity_map.values, color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        if selected_user == 'Overall':
            st.subheader('Most Active Users')
            x, percent_df = helper.fetch_most_active_users(df)

            col1, col2 = st.columns(2, gap="large")

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(percent_df)


        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji analysis
        emoji_df = helper.emojis_stats(selected_user, df)
        st.dataframe(emoji_df)

