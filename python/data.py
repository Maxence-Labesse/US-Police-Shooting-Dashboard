import pandas as pd
import os

path = os.path.dirname("shootings.csv")


class Data:

    def __init__(self):
        self.df = None

    def get_data(self):
        self.df = pd.read_csv(
            "data/shootings.csv",
            sep=",")

    @staticmethod
    def preprocess(df):
        df = df.assign(date=pd.to_datetime(df['date']))
        df = df.assign(year=df['date'].dt.year)
        # df = df.assign(week=df['date'].apply(lambda x: x.isocalendar()[1]))
        df = df.assign(crime=1)
        # df = df.assign(month_year=df['date'].dt.to_period('M'))
        df = df.assign(month_year=df['date'].dt.strftime('%y-%m'))
        df = df.loc[df["month_year"] != '2006']
        df = df.assign(armed=df['armed'].map(
            lambda x: x if x in ['gun', 'knife', 'unarmed', 'unknown'] else "other"))
        df = df.loc[df["month_year"] != '20-06']

        return df

    @staticmethod
    def age_groups(df):
        bins = [0, 18, 25, 35, 45, 55, 65, df.age.max()]
        labels = ['0-18', '18-25', '25-35', '35-45', '45-55', '55-65', '65+']

        return df.assign(age_group=pd.cut(df['age'], bins, labels=labels, include_lowest=True))

    @staticmethod
    def filter_df(df, years_vals=None, race='Overall'):
        assert (len(years_vals) is None or len(
            years_vals) == 2), "years_vals doit être None ou de la forme [year_min, year_max]"

        assert (years_vals is not None or race is not None), "Renseigner years_vals ou race"

        years = range(years_vals[0], years_vals[1] + 1, 1)
        if race == 'Overall':
            return df.loc[df["year"].isin(years)]
        else:
            return df.loc[(df["year"].isin(years) & (df["race"] == race))]

    @staticmethod
    def groupby_df_one(df, by, col_agg):
        df_agg = df.groupby([by]).agg({col_agg: 'sum'})
        df_agg = df_agg.sort_values(by=by)
        df_agg.reset_index(inplace=True)
        df_agg = df_agg.assign(race='overall')

        return df_agg

    @staticmethod
    def groupby_df_two(df, by1, by2, col_agg):
        idx = pd.MultiIndex.from_product((df[by1].unique(), df[by2].unique()))
        df_agg = df.groupby([by1, by2]).agg({col_agg: 'sum'}).reindex(idx)
        df_agg.fillna(0, inplace=True)
        df_agg.reset_index(inplace=True)
        df_agg.rename(columns={'level_0': by1, 'level_1': by2}, inplace=True)

        return df_agg

    @staticmethod
    def value_counts_1(df, by):
        df_val = df[by].value_counts()
        df_val = pd.DataFrame({by: df_val.index, "number": df_val.values})
        df_val.sort_values(by='number', ascending=False, inplace=True)

        return df_val


