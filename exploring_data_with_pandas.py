# Introduction to the Data
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # setting ignore as a parameter and further adding category

import pandas as pd
f500 = pd.read_csv('f500.csv',index_col=0)
f500.index.name = None

f500_head = f500.head(10)
print(f500.info())

#%%
# Vectorized Operations
rank_change = f500['previous_rank'] - f500['rank']
print(rank_change[0:5])

#%%
# Series Data Exploration Methods
rank_change_max = rank_change.max()
rank_change_min = rank_change.min()
print(rank_change_min, rank_change_max)

#%%
# Series Describe Method
rank = f500['rank']
rank_desc = rank.describe()
print(rank_desc)

prev_rank = f500['previous_rank']
prev_rank_desc = prev_rank.describe()
print(prev_rank_desc)

#%%
# Method Chaining - a way to combine multiple methods together in a single line
print(f500["country"].value_counts().loc["China"])

zero_previous_rank = f500["previous_rank"].value_counts().loc[0]
print(zero_previous_rank)

#%%
# Dataframe Exploration Methods
medians = f500[["revenues", "profits"]].median(axis=0)
# we could also use .median(axis="index")
# print(medians)

f500.info()
numeric_only = ['rank', 'revenues', 'revenue_change', 'profits', 'assets', 'profit_change', 'previous_rank', 'years_on_global_500_list', 'employees', 'total_stockholder_equity']
max_f500 = f500[numeric_only].max()
print(max_f500)

#%%
# Dataframe Describe Method
# By default, DataFrame.describe() will return statistics for only numeric columns.
#  If we wanted to get just the object columns, we need to use 'include=['O']' parameter
print(f500.describe(include=['O']))

f500_desc = f500.describe()
print(f500_desc)

#%%
# Assignment with pandas
top5_rank_revenue = f500[["rank", "revenues"]].head()
print(top5_rank_revenue)

top5_rank_revenue["revenues"] = 0
print(top5_rank_revenue)

top5_rank_revenue.loc["Sinopec Group", "revenues"] = 999
print(top5_rank_revenue)

print(f500.loc['Dow Chemical', 'ceo'])
f500.loc['Dow Chemical', 'ceo'] = 'Jim Fitterling'
print(f500.loc['Dow Chemical', 'ceo'])

#%%
# Using Boolean Indexing with pandas Objects
motor_bool = f500['industry'] == "Motor Vehicles and Parts"
motor_countries = f500.loc[motor_bool, 'country']
print(motor_countries)

#%%
# Using Boolean Arrays to Assign Values
ampersand_bool = f500["sector"] == "Motor Vehicles & Parts"
f500.loc[ampersand_bool,"sector"] = "Motor Vehicles and Parts"

f500.loc[f500["sector"] == "Motor Vehicles & Parts","sector"] = "Motor Vehicles and Parts"

import numpy as np
prev_rank_before = f500["previous_rank"].value_counts(dropna=False).head()
print(prev_rank_before)
prev_rank_bool = f500['previous_rank'] == 0
f500.loc[prev_rank_bool, 'previous_rank'] = np.nan
prev_rank_after = f500["previous_rank"].value_counts(dropna=False).head()
print(prev_rank_after)

#%%
# Creating New Columns
f500['rank_change'] = f500['previous_rank'] - f500['rank']
rank_change_desc = f500['rank_change'].describe()

#%%
# Challenge: Top Performers by Country
usa_bool = f500['country'] == 'USA'
industry_usa = f500.loc[usa_bool, 'industry'].value_counts()[0:2]
print(industry_usa)

china_bool = f500['country'] == 'China'
sector_china = f500.loc[china_bool, 'sector'].value_counts()[0:3]
print(sector_china)

#%%
import pandas as pd
# read the data set into a pandas dataframe
f500 = pd.read_csv("f500.csv", index_col=0)
f500.index.name = None

# replace 0 values in the "previous_rank" column with NaN
f500.loc[f500["previous_rank"] == 0, "previous_rank"] = np.nan

f500_selection = f500[['rank', 'revenues', 'revenue_change']].head(5)

#%%
# Reading CSV files with pandas
import pandas as pd
f500 = pd.read_csv('f500.csv')
f500.loc[f500["previous_rank"] == 0, "previous_rank"] = np.nan

#%%
# Using iloc to select by integer position
# loc: label based selection
# iloc: integer position based selection
fifth_row = f500.iloc[5]
company_value = f500.iloc[1,0]

first_three_rows = f500.iloc[0:3]
first_seventh_row_slice = f500.iloc[[0, 6], 0:5]

#%%
# Using pandas methods to create boolean masks
prev_is_null = f500["previous_rank"].isnull()
null_previous_rank = f500.loc[prev_is_null,["company","rank","previous_rank"]]

#%%
# Working with Integer Labels
null_previous_rank = f500[f500["previous_rank"].isnull()]
top5_null_prev_rank = null_previous_rank.iloc[0:5]

#%%
# Pandas Index AlignmentPandas Index Alignment
# A powerful aspect of pandas is that almost every operation will align
# on the index labels
previously_ranked = f500[f500["previous_rank"].notnull()]
rank_change = previously_ranked['previous_rank'] - previously_ranked['rank']
f500['rank_change'] = rank_change

#%%
# Using Boolean Operators
# We combine boolean arrays using boolean operators.
# pandas	Python equivalent	Meaning
# a & b	    a and b	            True if both a and b are True, else False
# a | b	    a or b	            True if either a or b is True
# ~a	    not a	            True if a is False, else False
large_revenue = f500['revenues'] > 100000
negative_profits = f500['profits'] < 0
combined = large_revenue & negative_profits
big_rev_neg_profit = f500[combined]

# same as above
combined = (f500["revenues"] > 100000) & (f500["profits"] < 0)
big_rev_neg_profit = f500[(f500["revenues"] > 100000) & (f500["profits"] < 0)]

brazil_venezuela = f500[(f500['country'] == 'Brazil') | (f500['country'] == 'Venezuela')]
tech_outside_usa = f500[(f500['sector'] == 'Technology') & (f500['country'] != 'USA')].head()

#%%
# Sorting Values
jpn = f500[(f500['country'] == 'Japan')]
sort_jpn = jpn.sort_values('employees', ascending=False)
top_japanese_employer = sort_jpn.iloc[0,0]

#%%
# Using Loops with pandas
# Aggregation is where we apply a statistical operation to groups of our data

# Create an empty dictionary to store the results
avg_rev_by_country = {}

# Create an array of unique countries
countries = f500["country"].unique()

# Use a for loop to iterate over the countries
for c in countries:
    # Use boolean comparison to select only rows that
    # correspond to a specific country
    selected_rows = f500[f500["country"] == c]
    # Calculate the mean average revenue for just those rows
    mean = selected_rows["revenues"].mean()
    # Assign the mean value to the dictionary, using the
    # country name as the key
    avg_rev_by_country[c] = mean

top_employer_by_country = dict()
countries = f500["country"].unique()
for c in countries:
    selected_rows = f500[f500["country"] == c]
    selected_rows_desc = selected_rows.sort_values('employees', ascending=False)
    top_co = selected_rows_desc.iloc[0, 0] # select first row in country column
    top_employer_by_country[c] = top_co

#%%
# Challenge: Calculating Return on Assets by Country
f500['roa'] = f500['profits'] / f500['assets']
sectors = f500["sector"].unique()

top_roa_by_sector = dict()
for sector in sectors:
    selected_rows = f500[f500["sector"] == sector]
    selected_rows_desc = selected_rows.sort_values('roa', ascending=False)
    top_co = selected_rows_desc.iloc[0, 0]
    top_roa_by_sector[sector] = top_co


