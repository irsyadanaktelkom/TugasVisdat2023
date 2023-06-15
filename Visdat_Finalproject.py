#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from bokeh.io import curdoc
from bokeh.models import Select, Slider
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
import streamlit as st

# Load the dataset
data = pd.read_csv('no_of_people_living_with_hiv_by_country_clean.csv')
data['Year'] = data['Year'].astype(str)  # Convert Year column to string type

# Convert 'Year' column to integer type
data['Year'] = data['Year'].astype(int)

# Create a Bokeh ColumnDataSource
source = ColumnDataSource(data=dict())

# Create a Bokeh figure
p = figure(x_range=[str(year) for year in data['Year'].unique()], plot_width=800, plot_height=400, title='HIV/AIDS Cases by Country')

# Create a CategoricalColorMapper to assign colors to countries
color_mapper = CategoricalColorMapper(factors=data['Country'].unique(), palette=Category10[10])

# Create a line_color transform using factor_cmap
line_color = factor_cmap(field_name='Country', palette=Category10[10], factors=data['Country'].unique())

# Add a line glyph for each country
p.multi_line(xs='Year', ys='Count', source=source, line_width=2, line_color=line_color)

# Define the callback function to update the plot based on user inputs
def update():
    country = select.value
    year = slider.value
    selected_data = data[(data['Country'] == country) & (data['Year'] == str(year))]
    source.data = dict(selected_data)

# Create a selection tool for countries
select_options = [(country, country) for country in data['Country'].unique()]
select = Select(title='Select Country', value=data['Country'].unique()[0], options=select_options)
select.on_change('value', lambda attr, old, new: update())

# Convert 'Year' column to integer type
data['Year'] = data['Year'].astype(int)

# Create a slider for years
slider = Slider(title='Select Year', start=int(data['Year'].min()), end=int(data['Year'].max()), value=int(data['Year'].min()), step=1)
slider.on_change('value', lambda attr, old, new: update())

# Initialize the plot
update()

# Create a Streamlit app
st.bokeh_chart(p, use_container_width=True)


# In[ ]:




