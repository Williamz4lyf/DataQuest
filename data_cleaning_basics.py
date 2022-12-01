# Reading CSV Files with Encodings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#%%

# common encodings: UTF-8, Latin-1 (also known as ISO-8859-1), Windows-1251
import pandas as pd
laptops = pd.read_csv("laptops.csv", encoding="Latin-1")
print(laptops.info())

#%%
# Cleaning Column Names
# Data CLeaning Workflow - Convert text to numeric dtype
# Explore the data in the column
# Identify patterns and special cases
# Remove non-digit characters
# Rename column if required
# Convert the column to a numeric dtype
col_names = laptops.columns

#%%
# Dont run

new_columns = list()
for name in col_names:
    name = name.strip()
    new_columns.append(name)

laptops.columns = new_columns
print(laptops.columns)

def clean_col_names(col_names):
    new_colnames = list()
    for name in col_names:
        name = name.strip()
        name = name.replace(' ', '_')
        name = name.replace('(', '').replace(')','')
        name = name.lower()
        new_colnames.append(name)

    return new_colnames

clean_col_names(col_names)

#%%
def clean_str(a_string):
    a_string = a_string.strip()
    a_string = a_string.replace('Operating System', 'os')
    a_string = a_string.replace(' ', '_')
    a_string = a_string.replace('(', '').replace(')','')
    a_string = a_string.lower()

    return a_string

new_colnames = list()
for col in laptops.columns:
    new_col = clean_str(col)
    new_colnames.append(new_col)

laptops.columns = new_colnames
print(laptops.columns)

#%%
def clean_col(col):
    col = col.strip()
    col = col.replace("(","")
    col = col.replace(")","")
    col = col.lower()
    return col

new_columns = []
for c in laptops.columns:
    clean_c = clean_col(c)
    new_columns.append(clean_c)

laptops.columns = new_columns
print(laptops.columns)

#%%
# Converting String Columns to Numeric
unique_ram = laptops['ram'].unique()

#%%
# Removing Non-Digit Characters
# The pandas library contains dozens of vectorized string methods we can use
# to manipulate text data, many of which perform the same operations as
# Python string methods.
# Pseudocode - Series.str.method_name()
laptops["screen_size"] = laptops["screen_size"].str.replace('"','')
print(laptops["screen_size"].unique())

laptops["ram"] = laptops["ram"].str.replace('GB','')
unique_ram = laptops["ram"].unique()
print(unique_ram)

#%%
# Converting Columns to Numeric Dtypes
laptops["screen_size"] = laptops["screen_size"].astype(float)
print(laptops["screen_size"].dtype)
print(laptops["screen_size"].unique())

laptops["ram"] = laptops["ram"].astype(int)

dtypes = laptops.dtypes
print(dtypes)

#%%
# Renaming Columns
laptops.rename({"screen_size": "screen_size_inches"}, axis=1, inplace=True)
laptops.rename({"ram": "ram_gb"}, axis=1, inplace=True)
ram_gb_desc = laptops['ram_gb'].describe()
print(laptops.dtypes)
print(ram_gb_desc)

#%%
# Extracting Values from Strings
laptops["gpu_manufacturer"] = (laptops["gpu"].str.split().str[0])
laptops["cpu_manufacturer"] = (laptops["cpu"].str.split().str[0])
cpu_manufacturer_counts = laptops["cpu_manufacturer"].value_counts()
print(cpu_manufacturer_counts)

#%%
# Correcting Bad Values - using series.map(dict)
mapping_dict = {'Android': 'Android', 'Chrome OS': 'Chrome OS', 'Linux': 'Linux',
                'Mac OS': 'macOS', 'No OS': 'No OS', 'Windows': 'Windows',
                'macOS': 'macOS'}
laptops['os'] = laptops['os'].map(mapping_dict)

#%%
# Dropping Missing Values
print(laptops.isnull().sum())

# There are a few options for handling missing values:
# Remove any rows that have missing values.
# Remove any columns that have missing values.
# Fill the missing values with some other value.
# Leave the missing values as is.

laptops_no_null_rows = laptops.dropna()
laptops_no_null_cols = laptops.dropna(axis=1)

#%%
# Filling Missing Values
print(laptops["os_version"].value_counts(dropna=False))
value_counts_before = laptops.loc[laptops["os_version"].isnull(), "os"].value_counts()
laptops.loc[laptops["os"] == "macOS", "os_version"] = "X"
laptops.loc[laptops["os"] == "No OS", "os_version"] = "Version Unknown"
value_counts_after = laptops.loc[laptops["os_version"].isnull(), "os"].value_counts()
print(value_counts_after)

#%%
# Challenge: Clean a String Column - weight columns
print(laptops["weight"].head())

laptops['weight'] = laptops['weight'].str.replace('kg','')
laptops['weight'] = laptops['weight'].str.replace('s','')
laptops['weight'] = laptops['weight'].astype(float)
laptops.rename(columns={'weight': 'weight_kg'}, inplace=True)

#%%
# Challenge
# Convert the price_euros column to a numeric dtype.
print(laptops["price_euros"].head())
laptops["price_euros"] = laptops["price_euros"].str.replace(',','.')
laptops['price_euros'] = laptops['price_euros'].astype(float)
print(laptops["price_euros"].head())

#%%
# Extract the screen resolution from the screen column.
print(laptops["screen"].head())

def screen_res(screen_string):
    screen_res_list = list()
    for item in screen_string:
        if len(item) > 1:
            new_item = item.split()
            screen_res_list.append(new_item[-1])
        else:
            screen_res_list.append(item)

    return screen_res_list

laptops['screen_resolution'] = screen_res(laptops['screen'])
print(laptops['screen_resolution'].head())

#%%
# Extract the processor speed from the cpu column.
# Use screen_res() function since the parameters are the same
print(laptops["cpu"].head())
laptops['cpu_processor_speed'] = screen_res(laptops["cpu"])
print(laptops["cpu_processor_speed"].head())

#%%
# Analysis Questions
# Are laptops made by Apple more expensive than those made by other manufacturers?
laptops.columns

top_manufacturers_by_price = dict()
manufacturers = laptops["manufacturer"].unique()
for m in manufacturers:
    selected_rows = laptops[laptops["manufacturer"] == m]
    mean = selected_rows['price_euros'].mean()
    top_manufacturers_by_price[m] = mean

print(top_manufacturers_by_price)
# on average, NO!

#%%
# What is the best value laptop with a screen size of 15" or more?
laptops['screen_size_inches'] = laptops['screen_size_inches'].astype(float)
fifteen_inch = laptops['screen_size_inches'] >= 15
print(laptops.loc[fifteen_inch, ['manufacturer', 'screen_size_inches','price_euros']].sort_values('price_euros'))

# Acer

#%%
# Which laptop has the most storage space?


#%%
laptops.to_csv('laptops_cleaned.csv', index_label=None)






