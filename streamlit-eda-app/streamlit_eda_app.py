# cheat sheet: https://docs.streamlit.io/library/cheatsheet

import streamlit as st
import pandas as pd
import numpy as np
import fastparquet as fp
import plotly.express as px
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio

st.header('Exploratory Data Analysis App')
st.markdown("" 
            'Python libraries: streamlit, numpy, pandas, plotly.'
            "")

# upload a file
file_bytes = st.file_uploader("Upload a file", type="csv")

# check the upload and read data
if file_bytes is not None:
    data = pd.read_csv(file_bytes)
    obj = []
    in_int = []
    in_float = []
    for i in data.columns:
        clas = data[i].dtypes
        if clas == 'object':
            obj.append(i)
        elif clas == np.int64:
            in_int.append(i)
        else:
            in_float.append(i)

# add submit button sidebar
with st.form(key = 'my_form'):
    with st.sidebar:
        st.sidebar.header('To remove Null valuues press below button')  
        submit_button = st.form_submit_button(label = 'Remove Null')     

# if need to replace null with mean and mode
if submit_button:
    for i in data.columns:
        clas = data[i].dtypes
        if clas == 'object':
            data[i].fillna(data[i].mode()[0], inplace=True) 
        else:
            data[i].fillna(data[i].mean(), inplace=True)   

# finding number of null values
lis = []
for i in data.columns:
    dd = sum(pd.isnull(data[i]))
    lis.append(dd)

 # if non of null values are zero, desplay test, else desplay bar plot for each column
if max(lis) == 0:
    st.write('Total no. of Null Values ' + str(max(lis)))
else:
    st.write('Bar plot to know no. of Null Values in each column')
    st.write('Total no. of Null Values ' + str(sum(lis)))
    fig = px.bar(x = data.columns, y = lis, labels = {'x': 'Column Names', 
                                                      'y': 'No. of Null Values'})
    st.plotly_chart(fig)

# frequency plot
st.sidebar.header('Select Variable')
selected_pos = st.sidebar.selectbox('Object Variables', obj)
st.write('Bar Plot to know frequency of each category')
frequency_data = data[selected_pos].value_counts()
fig = px.bar(frequency_data, x = frequency_data.index, y = selected_pos, 
             labels = {'x': selected_pos, 'y': 'count'})
st.plotly_chart(fig)

# histogram
st.sidebar.header('Select Variable')
selected_pos1 = st.sidebar.selectbox('Int or Float Variables', in_int+in_float)
st.write('Bar Plot to know count of values based on range')
counts, bins = np.histogram(data[selected_pos1], 
                            bins = range(int(min(data[selected_pos1])), 
                                         int(max(data[selected_pos1])),
                                         int(max(data[selected_pos1])/10))
                            )
bins = 0.5*(bins[:-1]+bins[1:])
fig = px.bar(x = bins, y = counts, 
             labels = {'x': selected_pos1, 'y': 'count'})
st.plotly_chart(fig)

# correlation chart
st.sidebar.header('Select Variable')
selected_pos2 = st.sidebar.multiselect('Int or Float Variable Correlation', in_int+in_float)
st.write('Scatter Plot for correlation')
if len(selected_pos2) == 2:
    fig = px.scatter(data, x = selected_pos2[0], y = selected_pos2[1])
    st.plotly_chart(fig)
else:
    st.write('Select Two Variables')