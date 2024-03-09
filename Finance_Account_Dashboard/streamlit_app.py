import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="P&L Dashboard",
    page_icon=":bar_chart:",
    layout="wide")

st.title("Profit & Loss Dashboard")
st.markdown("_Prototype v0.4.1_")

#create funtion drag and drop file before visaulize for users
@st.cache_data
def load_data(file):
    data= pd.read_excel(file)
    return data
#how to chosse layout https://docs.streamlit.io/library/api-reference/layout
upload_file = st.sidebar.file_uploader("Choose a file")

if upload_file is None:
    st.info("Upload a file through config",icon = "i")
    st.stop()

df = load_data(upload_file)
#hide the data frame in daata preview block with st expander
with st.expander("Data Preview"):
    st.dataframe(df)

# VISUALIZATION METHODS
#######################################

############ BAR 1 left top

import streamlit as st
import pandas as pd
import plotly.express as px

def plot_bar_revenue_chart(data, category_col, value_col, title):
    # Extract Total Revenue from iloc[5, 2]
    total_revenue = None
    if data.shape[0] > 5 and data.shape[1] > 2:
        total_revenue = data.iloc[5, 1]

    # Display st.metric for Total Revenue
    st.metric(label="Total Revenue", value=total_revenue)

    # Plot bar chart for the rest of the data
    fig = px.bar(data, x=category_col, y=value_col, title=title, color_discrete_map={'Actual': 'blue', 'Budget': 'orange'})
    # Add value labels on top of each bar
    fig.update_traces(text=data[value_col], textposition='outside')
    fig.update_layout(
        width=200,  # Set the width of the plot
        height=400,  # Set the height of the plot
        margin=dict(l=20, r=20, t=20, b=20),  # Adjust margin for positioning
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)

# Selecting specific rows based on condition (example: rows with index 0 and 1)
selected_rows = df.loc[[0, 1, 2, 3, 4, 5]]  # Include index 5 for Total Revenue

# Plot Bar Chart for selected rows with Actual and Budget side-by-side
plot_bar_revenue_chart(selected_rows, 'GL-CODE', 'Actual', 'Total Revenue')


################# BAR 1 right top
# Filter rows where 'GL-CODE' contains the word "Total"
total_rows = df[df['GL-CODE'].str.contains('Sales', case=False, na=False) & ~df['GL-CODE'].str.contains('Revenue', case=False, na=False)]


# Check if there are rows with "Total" in the 'GL-CODE' column
if not total_rows.empty:
    # Create a pie chart using the 'Actual' values for the filtered rows
    fig = px.pie(total_rows, values='Actual', names='GL-CODE', title='Actual Sales Distribution (GL-CODE)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No rows found with 'GL-CODE' containing the word 'Total'.")


################# BAR 2 left top
def plot_bar_chart(data, category_col, value_cols, title):
    if all(col in data.columns for col in value_cols):
        fig = px.bar(data, x=category_col, y=value_cols, title=title, barmode='group', color_discrete_map={'Actual': 'blue', 'Budget': 'orange'})
        
        # Add value labels on top of each bar
        for col in value_cols:
            fig.update_traces(text=data[col], textposition='outside', selector=dict(name=col))
        
        # Calculate the difference between 'Actual' and 'Budget' at row 5, column 3 if DataFrame has at least 6 rows
        if len(data) >= 6:
            data['Difference'] = data.iloc[5, 1] - data.iloc[5, 3]  # Assuming the 'Actual' column is at index 2 and 'Budget' column is at index 3
            # Add custom metric for the difference at index 5
            st.metric(label="P8 Total Revenue vs Expected Revenue", value=data['Difference'].iloc[5], delta=data['Difference'].iloc[5])
        else:
            st.warning("DataFrame does not have enough rows to calculate the difference at index 5.")
       
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Selected rows do not contain all required columns: {', '.join(value_cols)}")

# Selecting specific rows based on condition (example: rows with index 0 and 1)
selected_rows = df.loc[[0, 1, 2, 3, 4, 5]]

# Plot Bar Chart for selected rows with Actual and Budget side-by-side
plot_bar_chart(selected_rows, 'GL-CODE', ['Actual', 'Budget'], 'Total Revenue vs Expected Revenue')

############### bar 2 right top

def plot_bar_chart(data, category_col, value_cols, title):
    if all(col in data.columns for col in value_cols):
        fig = px.bar(data, x=category_col, y=value_cols, title=title, barmode='group', color_discrete_map={'Actual': 'blue', 'Budget': 'orange'})
        
        # Add value labels on top of each bar
        for col in value_cols:
            fig.update_traces(text=data[col], textposition='outside', selector=dict(name=col))
        
       
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Selected rows do not contain all required columns: {', '.join(value_cols)}")

# Selecting specific rows based on condition (example: rows with index 0 and 1)
selected_rows = df.loc[[6, 8, 10, 12, 20, 21, 25,28,29,47,56,60,65,67,68,74,77,78,79,80]]

# Plot Bar Chart for selected rows with Actual and Budget side-by-side
plot_bar_chart(selected_rows, 'GL-CODE', ['Actual', 'Budget'], 'Total Prime Cost & Operating Expense')



##### BAR 3 left top

# Filter rows where 'GL-CODE' contains the word "Total"
total_rows = df[df['GL-CODE'].str.contains('Labor', case=False, na=False)] #& ~df['GL-CODE'].str.contains('Revenue', case=False, na=False)]

# Check if there are rows with "Total" in the 'GL-CODE' column
if not total_rows.empty:
    # Create a pie chart using the 'Actual' values for the filtered rows
    fig = px.pie(total_rows, values='Actual', names='GL-CODE', title='Labor Distribution (Total 5200 - Salaries and Wages)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No rows found with 'GL-CODE' containing the word 'Total'.")


####### BAR 3 right top
import streamlit as st

# Assuming df is your DataFrame
# Selecting specific row based on index 81
selected_row = df.iloc[81]

# Display st.metric for Net Profit
net_profit_value = selected_row['Actual']  # Replace 'Actual' with the actual column name for Net Profit
st.metric(label="Net Profit", value=net_profit_value)

####### BAR 3 left

def plot_bar_chart(data, category_col, value_cols, title):
    if all(col in data.columns for col in value_cols):
        fig = px.bar(data, x=category_col, y=value_cols, title=title, barmode='group', color_discrete_map={'Actual': 'blue', 'Budget': 'orange'})
        
        # Add value labels on top of each bar
        for col in value_cols:
            fig.update_traces(text=data[col], textposition='outside', selector=dict(name=col))
        
        # Calculate the Net Profit at row 81, column 1 if DataFrame has at least 82 rows
        
       
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Selected rows do not contain all required columns: {', '.join(value_cols)}")

# Selecting specific rows based on condition (example: rows with index 81)
selected_rows = df.loc[[81]]

# Plot Bar Chart for selected rows with Actual and Budget side-by-side
plot_bar_chart(selected_rows, 'GL-CODE', ['Actual', 'Budget', 'YTD Actual', 'YTD Budget'], 'Net Profit')


########################### LAYOUT#########################

