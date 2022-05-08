
import pandas as pd

df = pd.read_excel(r'C:\temp\rd.xlsx',sheet_name='pct',usecols=[3,4])
print(df)

print('============================')

concat_func(df):

df2 = df.groupby(['姓'])['姓名'].apply()
df2 = df['SQ_FT'].astype('int').mean()
print(df2)

