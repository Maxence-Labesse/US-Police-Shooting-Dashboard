from python.data import Data
import pandas as pd

data = Data()
data.get_data()

#################
# preprocessing #
#################
data.df = data.df.assign(date_bis=pd.to_datetime(data.df['date']))
data.df = data.df.assign(year=data.df['date_bis'].dt.year)
data.df = data.df.assign(week=data.df['date_bis'].apply(lambda x: x.isocalendar()[1]))
data.df = data.df.assign(crime=1)
data.df = data.df.assign(month_year=data.df['date_bis'].dt.strftime('%y%m'))
data.df = data.df.loc[data.df["month_year"] != '2006']
print(data.df[['date', 'month_year', 'year', 'week', 'crime']].head(20))
print(data.df["race"].value_counts())

##############
# Parameters #
##############
years_val = [2016, 2019]

race = 'Black'

##############
# Filtered df
years = range(years_val[0], years_val[1] + 1, 1)

print(data.df['race'].unique().tolist())

df_filtered = data.df[data.df['year'].isin(years)]
df_filtered_race = df_filtered[df_filtered['race'] == race]


