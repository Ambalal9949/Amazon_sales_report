#!/usr/bin/env python
# coding: utf-8

# In[130]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 


# # Load dataset

# In[131]:


Amazon_sales = pd.read_csv(r"C:\Users\kings\OneDrive\MCA DATA SCIENCE\Innobyteproject\Amazon Sale Report.csv", encoding='ISO-8859-1')


# In[132]:


Amazon_sales.info()


# In[133]:


Amazon_sales.head()


# In[134]:


Amazon_sales.tail()


# In[135]:


# checking null values 
pd.isnull(Amazon_sales)


# In[136]:


# check total null values
pd.isnull(Amazon_sales).sum()


# In[137]:


Amazon_sales.shape


# In[138]:


# Fill nulls with specific values in specific columns
Amazon_sales['currency'].fillna(value='Unknown', inplace=True)
Amazon_sales['Amount'].fillna(value=0, inplace=True)


# In[139]:


Amazon_sales['ship-city'].fillna('Unknown', inplace=True)
Amazon_sales['ship-state'].fillna('Unknown', inplace=True)
Amazon_sales['ship-postal-code'].fillna('Unknown', inplace=True)
Amazon_sales['ship-country'].fillna('Unknown', inplace=True)


# In[140]:


Amazon_sales_filled = Amazon_sales.fillna(0)


# In[141]:


Amazon_sales.drop(columns=['New', 'PendingS'], inplace=True)


# In[142]:


print(pd.isnull(Amazon_sales).sum())


# In[143]:


Amazon_sales['fulfilled-by'].fillna('Unknown', inplace=True)


# In[144]:


print(pd.isnull(Amazon_sales).sum())


# In[145]:


Amazon_sales.shape


# In[146]:


Amazon_sales.info()


# In[147]:


Amazon_sales.head()


# In[148]:


print(Amazon_sales['ship-postal-code'].unique())


# In[149]:


Amazon_sales['ship-postal-code'] = pd.to_numeric(Amazon_sales['ship-postal-code'], errors='coerce').fillna(0).astype(int)


# In[150]:


Amazon_sales = Amazon_sales[pd.to_numeric(Amazon_sales['ship-postal-code'], errors='coerce').notna()]
Amazon_sales['ship-postal-code'] = Amazon_sales['ship-postal-code'].astype(int)


# In[151]:


print(Amazon_sales['ship-postal-code'].dtype)  # Should show 'int64'
print(Amazon_sales['ship-postal-code'].unique())  # Check the unique values


# In[152]:


Amazon_sales['Date'] = pd.to_datetime(Amazon_sales['Date'])


# In[153]:


Amazon_sales['Date'].dtype


# In[154]:


Amazon_sales.describe()


# In[155]:


#describe our data with object datatypes
Amazon_sales.describe(include='object')


# In[156]:


#describe for specific columns 
Amazon_sales[['Qty', 'Amount']].describe()


# In[157]:


Amazon_sales.head()


# In[158]:


ax=sns.countplot(x='Size', data=Amazon_sales)
#checking for data labels
for bars in ax.containers:
    ax.bar_label(bars)


# # Most of the people buys M-Size

# In[159]:


#courier status
plt.figure(figsize=(10,6))
sns.countplot(data = Amazon_sales,x='Courier Status',hue ='Status')
plt.show()


# # Majority to the orders are shipped through the courier 

# In[160]:


Amazon_sales.head()


# In[161]:


Amazon_sales.info()


# In[162]:


Amazon_sales['Category'] = Amazon_sales['Category'].astype(str)
c_d=Amazon_sales['Category']
plt.figure(figsize=(10,6))
plt.hist(c_d,bins=15,edgecolor="Black",color='yellow')
plt.xticks(rotation=90)
plt.show()


# # Most of the buyer are T-shirts 

# In[163]:


#checking B2B data 
check_B2B=Amazon_sales['B2B'].value_counts()

#create pie chart
plt.pie(check_B2B, labels=check_B2B, autopct='%1.1f%%')
plt.show()


# # Maximum 99.3% of buyers are retailers and 0.7% are wholesalers 

# In[164]:


#scatter plot
x_data = Amazon_sales['Category']
y_data = Amazon_sales['Size']

plt.scatter(x_data, y_data)
plt.xlabel('Category')
plt.ylabel('Size')
plt.title('Available Size')


# In[165]:


top10_sate=Amazon_sales['ship-state'].value_counts().head(10) #for top 10 states
plt.figure(figsize=(12,8))
sns.countplot(data=Amazon_sales[Amazon_sales['ship-state'].isin(top10_sate.index)],x="ship-state")
plt.xlabel('State')
plt.ylabel('Order_count')
plt.title('Distribustion of state')
plt.xticks(rotation=90)
plt.show()


# # Most of the buyers are MAHARASHTRA STATE
# 

# # 1. Sales Overview: 
# Analyze Sales Performance, Trends, and Patterns Over Time
# 
# You’ll want to use the Date, Status, Amount, and Qty columns to assess monthly sales patterns and cancellations.

# In[166]:


# Convert Date to a monthly period for aggregation
Amazon_sales['Year-Month'] = Amazon_sales['Date'].dt.to_period('M')


# In[167]:


# Sales Trends Over Time
monthly_sales = Amazon_sales.groupby('Year-Month')['Amount'].sum()
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Trends')
plt.xlabel('Year-Month')
plt.ylabel('Total Sales Amount')
plt.grid()
plt.show()


# In[168]:


# Analyzing Cancellations
cancellation_trends = Amazon_sales[Amazon_sales['Status'] == 'Cancelled'].groupby('Year-Month')['Order ID'].count()
plt.figure(figsize=(12, 6))
cancellation_trends.plot(kind='line', color='red', marker='x')
plt.title('Monthly Cancellations')
plt.xlabel('Year-Month')
plt.ylabel('Number of Cancellations')
plt.grid()
plt.show()


# In[169]:


import matplotlib.pyplot as plt

# Group by date and sum the amount
sales_trend = Amazon_sales.groupby('Date')['Amount'].sum().reset_index()

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(sales_trend['Date'], sales_trend['Amount'], marker='o')
plt.title('Total Sales Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales (INR)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()


# # 2. Product Analysis: 
# Popular Products by Category, Size, and Quantity Sold
# 
# Use Category, Size, and Qty to analyze popular products.

# In[170]:


# Top 10 Product Categories by Quantity Sold
top_categories = Amazon_sales.groupby('Category')['Qty'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_categories.index, y=top_categories.values, palette="viridis")
plt.title('Top 10 Product Categories by Quantity Sold')
plt.xlabel('Category')
plt.ylabel('Quantity Sold')
plt.xticks(rotation=90)
plt.show()


# In[171]:


# Size Distribution in Popular Categories
plt.figure(figsize=(12, 6))
sns.countplot(data=Amazon_sales, x='Size', order=Amazon_sales['Size'].value_counts().index, palette="coolwarm")
plt.title('Size Distribution')
plt.xlabel('Size')
plt.ylabel('Count')
plt.show()


# In[172]:


# Count of products sold by category
category_sales = Amazon_sales.groupby('Category')['Qty'].sum().sort_values(ascending=False)
print(category_sales)

# Average sales amount by product category
avg_sales_category = Amazon_sales.groupby('Category')['Amount'].mean()
print(avg_sales_category)


# # 3. Fulfillment Analysis: 
# Assess Fulfillment Methods and Courier Effectiveness
# 
# Use Fulfilment, Courier Status, and fulfilled-by for this analysis.

# In[173]:


# Fulfillment Method Effectiveness
fulfillment_counts = Amazon_sales['Fulfilment'].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=fulfillment_counts.index, y=fulfillment_counts.values, palette="viridis")
plt.title('Fulfillment Method Distribution')
plt.xlabel('Fulfillment Method')
plt.ylabel('Order Count')
plt.show()


# In[174]:


# Courier Status Analysis
plt.figure(figsize=(10, 6))
sns.countplot(data=Amazon_sales, x='Courier Status', hue='Fulfilment', palette="cool")
plt.title('Courier Status by Fulfillment Method')
plt.xlabel('Courier Status')
plt.ylabel('Count')
plt.show()


# In[175]:


# Count of orders fulfilled by each method
fulfillment_count = Amazon_sales['Fulfilment'].value_counts()
print(fulfillment_count)

# Average sales amount by fulfillment method
avg_sales_fulfillment = Amazon_sales.groupby('Fulfilment')['Amount'].mean()
print(avg_sales_fulfillment)


# # 4. Customer Segmentation: 
# Segment Customers by Behavior, Location, and Purchase Channel
# 
# Use Sales Channel, ship-city, ship-state, B2B, and other factors.

# In[176]:


# Sales Channel Segmentation
channel_distribution = Amazon_sales['Sales Channel'].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=channel_distribution.index, y=channel_distribution.values, palette="muted")
plt.title('Sales Channel Distribution')
plt.xlabel('Sales Channel')
plt.ylabel('Order Count')
plt.show()


# In[177]:


# B2B vs B2C Segmentation
plt.figure(figsize=(6, 6))
Amazon_sales['B2B'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#66b3ff', '#99ff99'])
plt.title('B2B vs B2C Distribution')
plt.show()


# In[178]:


# Sales by city
city_sales = Amazon_sales.groupby('ship-city')['Amount'].sum().sort_values(ascending=False)
print(city_sales)

# Count of products sold by size
size_sales = Amazon_sales.groupby('Size')['Qty'].sum().sort_values(ascending=False)
print(size_sales)


# # 5. Geographical Analysis: 
# Sales Distribution by States and Cities
# 
# Using ship-city, ship-state, and ship-country for geographic insights.

# In[179]:


# Top 10 States by Sales Volume
top_states = Amazon_sales.groupby('ship-state')['Amount'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_states.index, y=top_states.values, palette="coolwarm")
plt.title('Top 10 States by Sales Volume')
plt.xlabel('State')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.show()


# In[180]:


# Geographical Distribution by City (Top 10 Cities)
top_cities = Amazon_sales.groupby('ship-city')['Amount'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_cities.index, y=top_cities.values, palette="viridis")
plt.title('Top 10 Cities by Sales Volume')
plt.xlabel('City')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.show()


# In[181]:


# Total sales by state
state_sales = Amazon_sales.groupby('ship-state')['Amount'].sum().sort_values(ascending=False)
print(state_sales)

# Plotting sales by state
plt.figure(figsize=(12, 6))
state_sales.plot(kind='bar')
plt.title('Sales Amount by State')
plt.xlabel('State')
plt.ylabel('Total Sales Amount (INR)')
plt.xticks(rotation=90)
plt.grid()
plt.show()


# # 6. Business Insights and Recommendations
# Based on the findings above, consider actionable recommendations. For instance:
# 
# * Sales Growth: Identify high-demand periods and suggest marketing boosts during these times.
# * Product Focus: Increase stock of popular sizes and categories, such as T-shirts in size "M."
# * Fulfillment Improvement: Work on delivery effectiveness for specific fulfillment channels.
# * Customer Engagement: Focus on regions with high sales, offering location-specific discounts.
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




