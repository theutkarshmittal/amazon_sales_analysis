

import pandas as pd
import matplotlib.pyplot as plt

print("Understanding the dataset\n ")
df=pd.read_csv("Amazon Sale Report.csv")
print("Dataset shape:",df.shape)
print("No. of columns:",df.columns)
df.info()
print(df.describe(include="all"))# shows both numerical and categorical columns

print(df["Status"].value_counts())
print(df["Category"].value_counts()) # which category of products are mostly ordered


'''DATA CLEANING'''
print("\nData cleaning\n")

missing_value = df.isnull().sum().sort_values(ascending=False)
print("Missing values:",missing_value)

print(df.duplicated().sum())

print(df["Unnamed: 22"].value_counts(dropna=False)) # not useful for analysis
df.drop(columns=["Unnamed: 22"],inplace=True)
print(df.shape)
'''Removed a non-informative column (Unnamed: 22) containing a 
large proportion of missing values and no meaningful business information'''

print(df["ship-state"].nunique()) # it suggests that some states name appears in multiple form

print(sorted(df["ship-state"].dropna().unique()))

df_clean = df.copy()
df_clean["ship-state"] = df_clean["ship-state"].str.upper() # makes all states to uppercase
print(df_clean["ship-state"].nunique())
'''Performed data cleaning by standardizing categorical values and
 reducing inconsistent state entries from 69 to 47 unique values.'''

print(df_clean["ship-state"].dropna().unique())
df_clean["ship-state"]=df_clean["ship-state"].replace({
    "RAJSHTHAN": "RAJASTHAN",
    "RAJSTHAN" : "RAJASTHAN",
    "RJ" : "RAJASTHAN",
    "NEW DELHI" : "DELHI",
    "ORISSA" : "ODISHA",
    "PONDICHERRY": "PUDUCHERRY",
    "PB": "PUNJAB",
    "PUNJAB/MOHALI/ZIRAKPUR": "PUNJAB"
})
print(df_clean["ship-state"].nunique())
print(sorted(df_clean["ship-state"].dropna().unique()))


# data analysis

print("Data Analysis\n")

# which category has more revenue
category_revenue=df_clean.groupby("Category")["Amount"].sum().sort_values(ascending=False)
print(category_revenue)
''' well set and kurta have similar order values but there is a much difference in the 
revenue generated. Set have higher value indicating higher selling price '''

# Avg revenue made by each category
avg_rev=df_clean.groupby("Category")["Amount"].mean().sort_values(ascending=False)
print(avg_rev)
'''Set contributes the highest revenue not only because of high demand 
but also because its average order value (₹833) is significantly higher than Kurta (₹456).
Thats why set is more expensive than kurtas'''

# city vs revenue
city_rev=df_clean.groupby("ship-city")["Amount"].sum().sort_values(ascending=False).head(10)
print(city_rev)
'''Bengaluru, Hyderabad, and Mumbai emerged as the highest revenue-generating cities. 
Revenue was heavily concentrated in major metropolitan areas, 
indicating strong demand from urban customers and
 highlighting opportunities for targeted marketing and inventory optimization.'''

# state vs revenue
state_rev=df_clean.groupby("ship-state")["Amount"].sum().sort_values(ascending=False).head(10)
print(state_rev)

state_orders=df_clean["ship-state"].value_counts()
print(state_orders)
'''Maharashtra is the highest revenue-generating state and also has the highest order volume,
 suggesting that strong customer demand is a major driver of revenue in the region.'''

# avg order per state
state_avgrev=df_clean.groupby("ship-state")["Amount"].mean().sort_values(ascending=False).head(10)
print(state_avgrev)

# which fulfilment method generates more revenue
ful_rev=df_clean.groupby("Fulfilment")["Amount"].sum().sort_values(ascending=False)
print(ful_rev)
'''Amazon fulfilment contributed the majority of revenue,
generating more than twice the revenue of merchant fulfilment.
This indicates a strong dependence on Amazon's logistics network and
suggests that fulfilment efficiency plays a key role in sales performance.'''

# B2B analysis
business_to_business=df_clean.groupby("B2B")["Amount"].sum()
print(business_to_business)
'''More than 99% of orders and revenue come from B2C customers,
 indicating that the business is heavily dependent on
   individual consumers rather than corporate buyers.'''

# size distribution
size=df_clean["Size"].value_counts()
print(size)
'''Medium and Large sizes account for the highest share of orders, 
indicating strong customer demand for these sizes. 
Maintaining adequate inventory for these sizes can help
 reduce stockouts and improve sales performance.'''


# VISUALIZATION

# top 10 state revenue
plt.figure(figsize=(10,6))
plt.barh(state_rev.index, state_rev.values)
plt.title("Top 10 States by Revenue", color="purple", fontsize=15)
plt.xlabel("Revenue", fontsize=12, color="blue")
plt.ylabel("States", fontsize=12, color="blue")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("top_states_revenue.png")
plt.show()
''' Maharashtra generates the highest revenue and order volume,
making it the most valuable market in the dataset.
Karnataka and Telangana are also major revenue contributors.'''

# Top 10 categories by revenue
top_10_category=category_revenue.head(10)

plt.figure(figsize=(10,6))
plt.title("Top 10 Category by Revenue",color="purple",fontsize=15)
plt.xlabel("Revenue",fontsize=12,color="blue")
plt.ylabel("Category",fontsize=12,color="blue")
plt.barh(top_10_category.index , top_10_category.values)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("top_categories_revenue.png")
plt.show()
'''Set is the highest revenue-generating category, significantly outperforming other categories.
 This is driven by both high order volume and a higher average order value, 
 making it the most profitable product segment.'''

#Top 10 states by orders
top_10_states=state_orders.head(10)
plt.figure(figsize=(10,6))
plt.title("Top 10 States by Orders",color="purple",fontsize=15)
plt.xlabel("Orders",fontsize=12,color="blue")
plt.ylabel("States",fontsize=12,color="blue")
plt.barh(top_10_states.index , top_10_states.values)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("top_states_orders.png")
plt.show()
'''Revenue is concentrated in a few major states, with Maharashtra, Karnataka,
 and Telangana contributing the largest share. These regions represent high-value markets 
 where improving customer retention and expanding product availability could generate 
 significant business growth.'''

status_count = df_clean["Status"].value_counts().head(8)
print(status_count)
plt.figure(figsize=(10,5))
plt.title("Order status distribution", fontsize=15 , color="purple")
plt.xlabel("No. of orders",fontsize=12,color='blue')
plt.ylabel("order status",fontsize=12,color='blue')
plt.barh(status_count.index , status_count.values)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("order_status_distribution.png")
plt.show()
'''Most orders are successfully shipped or delivered, indicating an efficient fulfillment process.
Approximately 14% of orders were cancelled, representing a
potential area for operational improvement.
Returned orders form a small proportion of total orders, 
suggesting acceptable product quality and customer satisfaction.'''

'''The dataset shows a cancellation rate of approximately 14%,
which may indicate operational issues such as delivery delays,
inventory shortages, or customer-driven cancellations. 
Further investigation is required to identify the primary cause'''

# Which category cancelled the most
cancelled=df_clean[df_clean["Status"]=="Cancelled"]
print(cancelled["Category"].value_counts())