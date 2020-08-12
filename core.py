import seaborn as sns
import matplotlib as plt
import folium
from folium import Map
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap


def heatmap(gdf, location, lat, long):
    """
    This is a function that creates a heatmap.
    Parameters
    ----------
    gdf : geodata frame
    location : latitude and longitude (in list format) of central map location (e.g. NYC = [40.693943, -74.025])
    lat : dataset's column name for latitude (string)
    long: dataset's column name for latitude (string)

    Returns
    -------
    a heatmap of where a specific class of data is concentrated by sensor
    """
    latitude = lat
    longitude = long

    emptymap = Map(location=location, zoom_start=12)

    # create heatmap
    hm = HeatMap(
        list(zip(gdf.(latitude).values, gdf.(longitude).values)),
        min_opacity=0.2,
        radius=10,
        blur=13,
        max_zoom=1,
    )

    # add heatmap layer to empty layer
    emptymap.add_child(hm)
    return emptymap


def clustermap(gdf, location, lat, long):
    """
    This is a function that creates a cluster map.

    Parameters
    ----------
    gdf : geodata frame
    location : atitude and longitude (in list format) of central map location (e.g. NYC = [40.693943, -74.025])
    lat : dataset's column name for latitude (string)
    long : dataset's column name for longitude (string)

    Returns
    -------
    A cluster map of sensors

    """
    circlemap = folium.Map(location=location, zoom_start=12)

    # add marker for each sensor, use a clustered view (zoom in to see individual sensors)
    # added labels for each sensor which displays the sensor number and the counted occurence for music
    mc = MarkerCluster()
    for index, row in gdf.iterrows():
        mc.add_child(folium.Marker(location=[str(row[lat]), str(row[long])],
                                   clustered_marker=True))

    # add marker cluster layer to empty map
    circlemap.add_child(mc)
    return circlemap



def borough(df):
    """
    plot a pie chart of occurrence by borough
    Parameters
    ----------
    df : dataframe

    Returns
    -------
    a pie chart with occurrence of class in each borough
    """
    # find and tally occurrences in each borough
    borough_freq = df['borough'].value_counts()

    my_colors = ['lightcoral', 'moccasin', 'lightcyan']
    borough_freq.plot.pie(autopct='%1.1f%%', colors=my_colors)
    # noinspection PyUnresolvedReferences
    plt.title('Frequency of Music In Boroughs')
    # noinspection PyUnresolvedReferences
    plt.axis('equal')
    # noinspection PyUnresolvedReferences
    plt.figure(figsize=(2880, 288))
    # noinspection PyUnresolvedReferences
    return plt.show()



def year(df):
    """
    bar plot of sample occurrence by year
    Parameters
    ----------
    df

    Returns
    -------

    """
    sns.set(style="whitegrid")
    # noinspection PyUnresolvedReferences
    plt.title('Presence of Music from 2016-2019')
    return sns.countplot(x='year', data=df)



def week(df):
    """
    barplot of sample occurrence by week

    Parameters
    ----------
    df

    Returns
    -------

    """
    # noinspection PyUnresolvedReferences
    plt.figure(figsize=(15, 15))
    # noinspection PyUnresolvedReferences
    plt.title('Presence of Music By Week')
    return sns.countplot(x='week', data=df)



def day(df):
    """
    bar plot of sample occurrence by day

    Parameters
    ----------
    df

    Returns
    -------

    """
    # noinspection PyUnresolvedReferences
    plt.figure(figsize=(10, 10))

    # select colors
    colors = ['lightpink', 'lavender', 'lightblue', 'thistle', 'moccasin', 'lightgoldenrodyellow', 'honeydew']

    # count music frequency for each day
    ax = df['day'].value_counts()

    # plot data using information above
    # noinspection PyUnresolvedReferences
    plt.title('Presence of Music by Day')
    return ax.plot.pie(colors=colors, autopct='%.2f%%')



def hour(df):
    """
    barplot of sample occurrence by hour

    Parameters
    ----------
    df

    Returns
    -------

    """
    # noinspection PyUnresolvedReferences
    plt.figure(figsize=(15, 15))
    sns.set(style="whitegrid")
    # noinspection PyUnresolvedReferences
    plt.title('Presence of Music by Hour')
    return sns.countplot(x='hour', data=df)



def sensorbarplot(df, column):
    """
    mapping sensors to data barplot

    Parameters
    ----------
    df
    column

    Returns
    -------

    """
    col = str(column)
    # noinspection PyUnresolvedReferences
    plt.figure(figsize=(20, 20))
    # noinspection PyUnresolvedReferences
    plt.xlabel('Sensor')
    # noinspection PyUnresolvedReferences
    plt.ylabel('Music Presence Occurrence')
    return df.groupby('sensor_id')[col].count().plot.bar()
