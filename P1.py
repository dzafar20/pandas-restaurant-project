import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
order_df = pd.read_csv("order_details.csv",parse_dates=["order_date"]) 
order_df["order_time"] = pd.to_datetime(order_df["order_time"], format="%I:%M:%S %p").dt.time
#Cleaning the data by dropping rows with missing values
order_df = order_df.dropna ()
print(order_df.tail(10))
order_df.info()

#calling menu_df to get the menu details
menu_df = pd.read_csv("menu_items.csv")

print(menu_df.head(10))
menu_df.info()

# Merging the two dataframes to get a complete view of the orders and their details
merged_df = order_df.merge(menu_df, how="left", left_on="item_id", right_on="menu_item_id").drop(columns=["menu_item_id"])
merged_df.head()
print(merged_df.head(10))
merged_df.info()

#Adding tax and Revenue columns to the merged dataframe
merged_df["tax"] = merged_df["price"] * 0.08
merged_df["revenue"] = merged_df["price"] + merged_df["tax"]    

print(merged_df.head(20))
merged_df.head()

#Grouping best-selling and worst selling items by item_id and calculating total revenue for each item
merged_df.query("category == 'Italian'").groupby("item_name").agg({"revenue": "sum"}).sort_values("revenue").plot.barh()

#plot.barh()

#Analzying busiest time
plt.figure()
merged_df["hour"] = pd.to_datetime(merged_df["order_time"].astype(str)).dt.hour
merged_df.groupby("hour")["revenue"].size().plot()

plt.show()

merged_df["day_of_week"] = merged_df["order_date"].dt.dayofweek
merged_df.head()

#Transfrm data in pivot table
# Heatmap: revenue by hour and day of week
plt.figure(figsize=(10, 8))   # fresh canvas, nice size
sns.heatmap(
    merged_df.pivot_table(
        index="hour",
        columns="day_of_week",
        values="revenue",
        aggfunc="sum"
    ),
    annot=True,
    fmt=".0f",        # round numbers, no decimals
    cmap="vlag"     # color scheme: Blue → Grey → Red
)
plt.title("Revenue Heatmap: Hour vs Day of Week")
plt.tight_layout()
plt.savefig("heatmap.png")
plt.show()