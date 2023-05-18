import requests
import time
import pandas as pd
import calendar
import numpy as np

# Define the Slack webhook URL
WEBHOOK_URL = "https://hooks.slack.com/services/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"


# Function to send a message to Slack
def send_slack_message(message):
    data = {"text": message}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 200:
        print("Failed to send message to Slack")

# Analyze and summarize the data

df = pd.read_excel(r'C:\Users\USER\Downloads\covid-19-state-level-data.xlsx')
df['month'] = df['date'].dt.month
df_new = df[df['month'].isin([3,4,5,6])]
res = df_new.groupby(['month','state'])['deaths'].sum()
result_df = res.reset_index().groupby('month').apply(lambda x: x.nlargest(3, 'deaths')).reset_index(drop = True)
total_deaths = df_new.groupby('month')['deaths'].sum().to_dict()
result_df['%_of_tot'] = result_df.apply(lambda x : np.round(x['deaths']/total_deaths[x['month']],2),axis = 1 )


def creating_and_sending_message():
    message = ''
    for month,summary in result_df.groupby('month'):
        message = f'''Month - {calendar.month_name[month]}
    {summary['state'].iloc[0]} - {summary['deaths'].iloc[0]}, {summary['%_of_tot'].iloc[0]}%
    {summary['state'].iloc[1]} - {summary['deaths'].iloc[1]}, {summary['%_of_tot'].iloc[1]}%
    {summary['state'].iloc[2]} - {summary['deaths'].iloc[2]}, {summary['%_of_tot'].iloc[2]}%
                '''    
        send_slack_message(message)
        time.sleep(120)   # creating a time period of 2 minutes of interval, for the next message to be sent


# call the function
creating_and_sending_message()
