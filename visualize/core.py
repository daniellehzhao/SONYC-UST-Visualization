# This is a function that takes in a dataset, list of columns or a column, and a specific class that one would want to focus on.
# It creates a df that reads in the data set, drops columns provided by delcolumns, deletes rows from other columns that are not relevant and prints part of the df.
def clean(file, delcolumns, trueclass):
    df = pd.read_csv(file)
    df = df.drop(columns = columns)
    df = df.reset_index()
    df = df[df[truecol] == True]
    df.head()
    return(df)


# This is a function that creates a heatmap. It's parameters are a geo dataframe, central location of the map for display, and the lat/long column
def heatmap(gdf, location, lat, long):
    # set map location, creaty empty map
    heatmap = Map(location=location, zoom_start=12)

    # create heatmap
    hm = HeatMap(
        list(zip(gdf.lat.values, gdf.long.values)),
        min_opacity=0.2,
        radius=10,
        blur=13,
        max_zoom=1,
    )

    # add heatmap layer to empty layer
    heatmap.add_child(hm)
    return(heatmap)


# This is a function that creates a cluster map. It's parameters are a geo dataframe, central location of the map for display, and the lat/long column names which must be strings
def clustermap(gdf, location, lat, long):
    circlemap = folium.Map(location=location, zoom_start=12)

    # add marker for each sensor, use a clustered view (zoom in to see individual sensors)
    # added labels for each sensor which displays the sensor number and the counted occurence for music
    mc = MarkerCluster()
    for index, row in gdf.iterrows():
        mc.add_child(folium.Marker(location=[str(row[lat]), str(row[long])],
                                   clustered_marker=True))

    # add marker cluster layer to empty map
    circlemap.add_child(mc)
    return(circlemap)

#plot a pie chart of occurence by borough
def borough(df):
    # find and tally occurrences in each borough
    borough_freq = df['borough'].value_counts()

    my_colors = ['lightcoral', 'moccasin', 'lightcyan']
    borough_freq.plot.pie(autopct='%1.1f%%', colors=my_colors)
    plt.title('Frequency of Music In Boroughs')
    plt.axis('equal')
    plt.figure(figsize=(2880, 288))
    return(plt.show())

#barplot of sample occurence by year

def year(df):
    yearfreq = sns.set(style="whitegrid")
    yearfreq = sns.countplot(x='year', data=musicdf2)
    plt.title('Presence of Music from 2016-2019')
    return(yearfreq)
