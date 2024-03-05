import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
days_df = pd.read_csv("day.csv", delimiter=",")
hours_df = pd.read_csv("hour.csv", delimiter=",")
data_df = pd.merge(left=days_df, right=hours_df, how="left")

# Data preprocessing
data_df['dteday'] = pd.to_datetime(data_df['dteday'])
data_df['season'] = data_df.season.astype('category')
data_df['mnth'] = data_df.mnth.astype('category')
data_df['holiday'] = data_df.holiday.astype('category')
data_df['weekday'] = data_df.weekday.astype('category')
data_df['workingday'] = data_df.workingday.astype('category')
data_df['weathersit'] = data_df.weathersit.astype('category')

data_df.season.replace((1, 2, 3, 4), ('Winter', 'Spring', 'Summer', 'Fall'), inplace=True)
data_df.yr.replace((0, 1), (2011, 2012), inplace=True)
data_df.mnth.replace((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
                     ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), inplace=True)
data_df.weathersit.replace((1, 2, 3, 4), ('Clear', 'Misty', 'Light_RainSnow', 'Heavy_RainSnow'), inplace=True)
data_df.weekday.replace((0, 1, 2, 3, 4, 5, 6), ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), inplace=True)
data_df.workingday.replace((0, 1), ('No', 'Yes'), inplace=True)
data_df.rename(columns={"dteday": "date", "yr": "year", "mnth": "month", "weathersit": "weather", "hum": "humidity",
                        "cnt": "total_count"}, inplace=True)
data_df['temp'] = data_df['temp'] * 41
data_df['atemp'] = data_df['atemp'] * 50
data_df['humidity'] = data_df['humidity'] * 100
data_df['windspeed'] = data_df['windspeed'] * 67

# Streamlit App
st.title('Bikeshare Data Exploration')

# Data exploration section
if st.checkbox('Show data'):
    st.write(data_df.head())

# Histograms section
st.header('Histograms')
columns = ['casual', 'registered']
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
for i, column in enumerate(columns):
    axes[i].hist(data_df[column], bins=10, color='blue')
    axes[i].set_title(column)
    axes[i].set_xlabel(column)
    axes[i].set_ylabel('Frequency')
st.pyplot(fig)

# Boxplots section
st.header('Boxplots')
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
for i, column in enumerate(columns):
    ax[i].boxplot(data_df[column], vert=False, patch_artist=True, boxprops=dict(facecolor='red'))
    ax[i].set_title(column)
    ax[i].set_xlabel("")
    ax[i].set_ylabel("")
st.pyplot(fig)

# Total rides by season section
st.header('Total bikeshare rides per Season')
plt.figure(figsize=(10, 6))
seasonal_data = data_df.groupby(['season', 'year'])['total_count'].sum().unstack()
for year in seasonal_data.columns:
    plt.bar(seasonal_data.index, seasonal_data[year], label=str(year))
plt.xlabel("Season")
plt.ylabel("Total Rides")
plt.title("Total bikeshare rides per Season")
plt.legend(title='Year')
st.pyplot()

# Total rides by month section
st.header('Total bikeshare rides per Month')
plt.figure(figsize=(10, 6))
monthly_data = data_df.groupby(['month', 'year'])['total_count'].sum().unstack()
for year in monthly_data.columns:
    plt.bar(monthly_data.index, monthly_data[year], label=str(year))
plt.xlabel("Month")
plt.ylabel("Total Rides")
plt.title("Total bikeshare rides per Month")
plt.legend(title='Year')
st.pyplot()
