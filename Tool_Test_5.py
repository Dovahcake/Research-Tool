#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import streamlit as st


# In[2]:


file = Dataset("Tool Files/Default run.nc") # Read in the file
Loop_list = list(file.variables.keys()) # Creating a list of the variable names to iterate through
char = st.text_input(label="Please input an element or species of interest. Case sensitive.")
        


# In[3]:


Variables = {} # Creating an empty dictionary to store the new variables of interest
Variables_l = [] # Creating a list to do the same. Inefficient but solves a later issue.
Interest = 0 # Creating a variable to add the concentrations of the species of interest to

count = 0

for x in Loop_list:
    if char in x: # Checking for target character
        Variables[count] = x # Adds name of variable that fulfills the criteria to the new dictionary. Useful for later
        count = count + 1 # Prepares next variable to be checked
        Variables_l.append(x) 
        Interest = Interest + file.variables[x][:] # At the end of the loop this will contain the total Xx concentration. 
                                                   # Easier to do it this way round and remove indivudal species later


# In[4]:


st.title('The Concatenator')
st.sidebar.markdown('Species') # Creates a sub-heading on the side for the below checkbox sections.
selected_species = [
    species_name for species_number, species_name in Variables.items() #  Converts dictionary into an editable list 
    if st.sidebar.checkbox(species_name, True)] # Only checked species count towards selected species
print(selected_species)
for x in Variables_l: # Need to iterate through the list, the dictionary has no matching elements due to the count variable associated with it
    if x not in selected_species: 
        Interest = Interest - file.variables[x][:] # Untick recalculates interest for remaining variables, ticking again automatically adds it back
if Interest.mean() == 0: # 
    st.error("Please select at least one species present in the file")


# In[5]:


lat = file.variables['lat'][:] # Defining latitude and longitude variables to plot against
lon = file.variables['lon'][:]
plot = Interest[0][0][:][:] # Narrowing down the array shape without taking the mean
plot, lon = add_cyclic_point(plot, coord=lon) # Ensures the data points at lon=0 are included so no white line in the middle
# is present. From https://stackoverflow.com/questions/56348136/white-line-in-contour-plot-in-cartopy-on-center-longitude

fig = plt.figure(figsize=(20,30)) # Plot setup
ax1 = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
im1 = ax1.contourf(lon, lat, plot, cmap="plasma")
ax1.coastlines() 
ax1.set_title("Total " + char + "x Concentration")
cax = fig.add_axes([0.15, 0.3, 0.7, 0.05]) # Making a colorbar to the side of the plot
cbar = fig.colorbar(im1, cax=cax, orientation="horizontal") # Assigning the colours of the colourbar to match the plot data
st.pyplot(fig) # Above plot conditions are displayed in streamlit

