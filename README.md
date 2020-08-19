# SONYC-UST-Visualization

This repository contains the sonyc_visualization package which was created to be used for temporal and spatial analysis specifically on SONYC-UST data as well as specific examples demonstrating the use of each function. Functions allow for the creation of plots such as heatmaps, clustermaps, and various barplots which look at the relationship between specific classes and time/location. Additionally, the user can use sonyc_visualization to load a csv into a pandas dataframe and GeoDataFrame which are necessary for the use of other functions.

## Getting Started

Examples: https://github.com/daniellehzhao/SONYC-UST-Visualization/blob/master/examples/sonyc_ust_exploration.ipynb

### Installing
Included in this repo is a requirements.txt file which will simplify the process of recreating an environment with all necessary packages (pandas, seaborn, matplotlib, geopandas, and folium). 

1. Create/activate your conda environment. 
documentation on how to do this: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

2. Install packages using requirements.txt  
<pre><code>pip install -r requirements.txt</code></pre>

(You will have to make sure that pip is up to date)
