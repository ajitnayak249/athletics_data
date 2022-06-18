import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("download-removebg-preview.png")
user_menu = st.sidebar.radio(
    "Select An Option",
    ("Medal Tally", "Overall Analysis", "Country-Wise Analysis", "Athlete Wise Analysis")
)


if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")

    year, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country + " Overall Performance")
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1 , col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Host")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Athletes")
        st.title(athletes)

    with col3:
        st.header("Nations")
        st.title(nations)


    nations_over_time = helper.data_over_time(df, "region")
    fig = px.line(nations_over_time, x="Editions", y="region")
    st.title("Participateing Nations Over The Year")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, "Event")
    fig = px.line(events_over_time, x="Editions", y="Event")
    st.title("Event Over The Year")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athlete_over_time, x="Editions", y="Name")
    st.title("Athletes Over The Year")
    st.plotly_chart(fig)

    st.title("No. Of Events Over Time(Every Sport)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athelets")
    sport_list  = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    Selected_sport= st.selectbox('Select A Sport', sport_list)
    x = helper.most_successful(df, Selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':

    st.sidebar.title('Country-Wise Analysis')
    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select A Country", country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally Over The Year")
    st.plotly_chart(fig)

    st.title(selected_country + " excel in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(15, 15))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)


if user_menu == "Athlete Wise Analysis":
    athelets_df = df.drop_duplicates(subset=["Name", "region"])
    x1 = athelets_df["Age"].dropna()
    x2 = athelets_df[athelets_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athelets_df[athelets_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athelets_df[athelets_df["Medal"] == "Bronze"]["Age"].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.title("Distribution Of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery','Modern Pentathlon',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athelets_df[athelets_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution Of Age With Respect To Sports(Gold Medalist)")
    st.plotly_chart(fig)

    for sport in famous_sports:
        temp_df = athelets_df[athelets_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Silver"]["Age"].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution Of Age With Respect To Sports(Silver Medalist)")
    st.plotly_chart(fig)



    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title("Height vs Weight")
    Selected_sport = st.selectbox('Select A Sport', sport_list)

    temp_df = helper.weight_vs_height(df, Selected_sport)
    fig = px.scatter(temp_df, x="Weight", y=["Height"], color="Medal", symbol="Sex")
    fig.update_layout(autosize=False, width=1200, height=800)
    st.plotly_chart(fig)


    st.title("Men vs Women Participate Over The Year.")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Men", "Women"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)