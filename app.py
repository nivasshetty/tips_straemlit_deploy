import streamlit as st # type: ignore
import pandas as pd # type: ignore
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt # type: ignore
import json

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("tips.csv")    # Use your downloaded tips CSV

st.title("📊 Tips Data Dashboard (Streamlit)")
st.write("Interactive dashboard built using Streamlit and Tips dataset.")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

# Filter: Day of the week
day_filter = st.sidebar.selectbox(
    "Select Day:",
    options=["All"] + list(df["day"].unique())
)

# Filter: Time
time_filter = st.sidebar.selectbox(
    "Select Time:",
    options=["All"] + list(df["time"].unique())
)

# Filter: Tip Amount Slider
max_tip = float(df["tip"].max())
tip_range = st.sidebar.slider(
    "Tip Amount Range:",
    0.0, max_tip, (0.0, max_tip)
)

# Apply filters
filtered_df = df.copy()

if day_filter != "All":
    filtered_df = filtered_df[filtered_df["day"] == day_filter]

if time_filter != "All":
    filtered_df = filtered_df[filtered_df["time"] == time_filter]

filtered_df = filtered_df[
    (filtered_df["tip"] >= tip_range[0]) &
    (filtered_df["tip"] <= tip_range[1])
]

# ----------------------------
# Display Data
# ----------------------------
st.subheader("📄 Filtered Data Table")
st.dataframe(filtered_df)

# ----------------------------
# JSON Output
# ----------------------------
st.subheader("📦 JSON Output")
st.json(json.loads(filtered_df.to_json(orient="records")))

# ----------------------------
# Plots
# ----------------------------
st.subheader("📈 Visualizations")

plot_type = st.selectbox(
    "Choose a plot type:",
    ["Histogram - Total Bill", "Scatterplot - Total Bill vs Tip", "Boxplot - Tips by Day"]
)

fig, ax = plt.subplots(figsize=(8, 4))

if plot_type == "Histogram - Total Bill":
    ax.hist(filtered_df["total_bill"], bins=20)
    ax.set_title("Distribution of Total Bill")
    ax.set_xlabel("Total Bill")
    ax.set_ylabel("Frequency")

elif plot_type == "Scatterplot - Total Bill vs Tip":
    ax.scatter(filtered_df["total_bill"], filtered_df["tip"])
    ax.set_title("Total Bill vs Tip")
    ax.set_xlabel("Total Bill")
    ax.set_ylabel("Tip")

else:
    filtered_df.boxplot(column="tip", by="day", ax=ax)
    ax.set_title("Tips by Day")
    ax.set_ylabel("Tip Amount")

st.pyplot(fig)

# ----------------------------
# Footer
# ----------------------------
st.write("---")
st.write("Built with ❤ using Streamlit")