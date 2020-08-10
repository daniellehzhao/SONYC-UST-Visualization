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
    sns.set(style="whitegrid")
    plt.title('Presence of Music from 2016-2019')
    return(sns.countplot(x='year', data=df))

#barplot of sample occurence by week
def week(df):
    plt.figure(figsize=(15, 15))
    plt.title('Presence of Music By Week')
    return(sns.countplot(x='week', data=df))


#barplot of sample occurence by day
def day(df):
    plt.figure(figsize=(10,10))

    #select colors
    colors = ['lightpink','lavender','lightblue', 'thistle', 'moccasin','lightgoldenrodyellow', 'honeydew']

    #count music frequency for each day
    ax = df['day'].value_counts()

    #plot data using information above
    plt.title('Presence of Music by Day')
    return(ax.plot.pie(colors = colors, autopct='%.2f%%'))

#barplot of sample occurence by hour
def hour(df):
    plt.figure(figsize=(15, 15))
    sns.set(style="whitegrid")
    plt.title('Presence of Music by Hour')
    return(sns.countplot(x='hour', data=df))


#mapping sensors to data barplot
def sensorbarplot(df, column):
    col = str(column)
    plt.figure(figsize =(20,20))
    plt.xlabel('Sensor')
    plt.ylabel('Music Presence Occurrence')
    return(df.groupby('sensor_id')[col].count().plot.bar())