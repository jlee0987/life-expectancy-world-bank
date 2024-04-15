#Data Download

import requests

url = 'https://www.kaggle.com/datasets/mjshri23/life-expectancy-and-socio-economic-world-bank/download?datasetVersionNumber=1'

response=requests.get(url)
with open('life_expectancy.csv', 'w') as f:
  if response.ok:
		f.write(response.content)
	print('finished writing')

#Data Cleaning - filtering for data from 2019 only
import pandas as pd
df=pd.read_csv('file:///Users/jillianlee/Downloads/life%20expectancy.csv')
df.drop(columns=['Country Code', 'Injuries'], inplace=True)
df_2019=df.loc[df['Year'] == 2019]
df_new=df_2019.dropna(axis=0, subset=['Life Expectancy World Bank'])
print(df_new)

#Minimum and Maximum Life Expectancy - by Region
result=df_new.groupby('Region').agg({'Life Expectancy World Bank': ['min', 'max']})
print(result)

#Sorted List of Life Expectancy - by Country
result=df_new.groupby('Life Expectancy World Bank')['Country Name'].sum()
print(result)

#Range in Terms of Life Expectancy - by Region
df_new.groupby('Region').apply(lambda x: x['Life Expectancy World Bank'].max() - x['Life Expectancy World Bank'].min())

#Range in Terms of Life Expectancy - by Income Group
df_new.groupby('IncomeGroup').apply(lambda x: x['Life Expectancy World Bank'].max() - x['Life Expectancy World Bank'].min())

#Mean Life Expectancy - overall, by Region and by Income Group
df_new['Life Expectancy World Bank'].mean()

region=df_new.groupby(['Region'])['Life Expectancy World Bank'].mean()
print(region)

income=df_new.groupby(['IncomeGroup'])['Life Expectancy World Bank'].mean()
print(income)

#Bar Charts - Mean Life Expectancy by Region and by Income Group
region_plot=region.plot.barh(x='Region', y='Mean Life Expectancy')
region_plot.bar_label(region_plot.containers[0])
plt.title('Mean Life Expectancy by Region')
plt.show()

income_plot=income.plot.barh(x='Income Group', y='Mean Life Expectancy')
income_plot.bar_label(income_plot.containers[0])
plt.title('Mean Life Expectancy by Income Group')
plt.show()

#Scatterplot - Life Expectancy vs. Health Expenditure (%)
import seaborn as sns
fig,ax=plt.subplots(figsize=(6,4))
colors={'East Asia & Pacific': 'red', 'South Asia': 'pink','Europe and Central Asia': 'cyan','Latin America & Caribbean': 'green', 'Middle East & North Africa': 'yellow', 'North America':'brown', 'Sub-Saharan Africa': 'purple'}
sns.scatterplot(data=df_new, x='Health Expenditure %', y='Life Expectancy World Bank', hue='Region',palette=colors,ax=ax)
ax.set(xlabel='Health Expenditure %', ylabel='Life Expenditure World Bank')
fig.suptitle('Life Expectancy vs Health Expenditure %')
plt.show()

#Kernel Density Estimate (KDE) Plot - Observations in terms of Life Expectancy
df_new['Life Expectancy World Bank'].plot(kind='kde')
plt.suptitle('Distribution of Observations – Life Expectancy')
plt.show()

#Ranking and Bar Charts- Top 10 and Bottom 10 Countries by Life Expectancy
top_10=df_new.nlargest(10,['Life Expectancy World Bank'])
print(top_10)

top_10_plot=top_10.plot.barh(x='Country Name', y='Life Expectancy World Bank')
top_10_plot.bar_label(top_10_plot.containers[0])
top_10_plot.invert_yaxis()
plt.title('Top 10 Countries by Life Expectancy')
plt.show()

bottom_10=df_new.nsmallest(10,['Life Expectancy World Bank'])
print(bottom_10)

bottom_10_plot=bottom_10.plot.barh(x='Country Name', y='Life Expectancy World Bank')
bottom_10_plot.bar_label(bottom_10_plot.containers[0])
bottom_10_plot.invert_yaxis()
plt.title('Bottom 10 Countries by Life Expectancy')
plt.show()

#Median Percentage Spent on Healthcare - 2010 - 2019
#Median Percentage over same period, grouped by Region and by Income Group

df_2010_2019=df.loc[df['Year']>=2010].loc [df['Year']<=2019]
df_new= df_2010_2019.dropna(axis=0, subset=['Life Expectancy World Bank'])
 
result=df_new.groupby(['Region'])['Health Expenditure %'].median()
print ('Median expenditure on health as a percentage of GDP – by Region')
print(result)

df_new.groupby(['Region','IncomeGroup'])['Health Expenditure %'].median() 

#CO2 Emissions (Megatons) for Countries with Life Expectancy lower than 60 years
df_filtered=df.loc[(df['Year'] == 2019) & (df['Life Expectancy World Bank']<60)]
 result=df_new.groupby(['Country Name'])['CO2'].sum()
print(result//1000)
mean= (df_new['CO2'].mean())//1000
print(mean)

#CO2 Emissions (Megatons) for Countries with Life Expectancy greater than 75 years
df_filtered=df.loc[(df['Year'] == 2019) & (df['Life Expectancy World Bank']>75)]
df_new=df_filtered.dropna(axis=0, subset=['Life Expectancy World Bank'])
df_new2=df_new.dropna(axis=0, subset=['CO2'])
df_new3=df_new2.groupby(['Country Name'])['CO2'].sum()
print(df_new3//1000)
mean=(df_new3.mean())//1000
print(mean)

#Pearson Correlation Coefficient Matrix and Heatmap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('file:///Users/jillianlee/Downloads/life%20expectancy.csv')
df.drop(columns=['Country Code', 'Injuries'], inplace=True)
df_2019=df.loc[df['Year']==2019]
df_new=df_2019.dropna(axis=0,subset=[‘Life Expectancy World Bank’])
pd.set_option('display.max_rows’,100)
pd.set_option('display.max_columns’,100)

pearsoncorr=df_new.corr(method=‘pearson’,numeric_only=True)
pearsoncorr
sns.heatmap(pearsoncorr, xticklabels=pearsoncorr.columns, yticklabels=pearsoncorr.columns, cmap='RdBu_r', annot=True, linewidth=0.5)
plt.title('Correlation Heatmap – Life Expectancy Dataset (2019)')
plt.show()
