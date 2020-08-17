import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import geopandas as gpd
from folium import Map
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap


def load_df(csv, classes, main_class=None):
    """
    loads data by taking out unnecessary columns and only counting occurrences that are true

    Parameters
    ----------
    csv (string) : path or name of csv file
    classes (list) : desired class and subclass column names
    main_class (string): name of the working overarching class. If not specified, the dataframe will not check for
    occurrences of the given class that are true and will not remove false ones

    Returns
    -------
    dataframe that only contains desired columns of classes/subclasses

    """
    col1 = ['annotator_id', '1-1_small-sounding-engine_presence',
            '1-2_medium-sounding-engine_presence',
            '1-3_large-sounding-engine_presence',
            '1-X_engine-of-uncertain-size_presence', '2-1_rock-drill_presence',
            '2-2_jackhammer_presence', '2-3_hoe-ram_presence',
            '2-4_pile-driver_presence',
            '2-X_other-unknown-impact-machinery_presence',
            '3-1_non-machinery-impact_presence', '4-1_chainsaw_presence',
            '4-2_small-medium-rotating-saw_presence',
            '4-3_large-rotating-saw_presence',
            '4-X_other-unknown-powered-saw_presence', '5-1_car-horn_presence',
            '5-2_car-alarm_presence', '5-3_siren_presence',
            '5-4_reverse-beeper_presence',
            '5-X_other-unknown-alert-signal_presence', '6-1_stationary-music_presence', '6-2_mobile-music_presence',
            '6-X_music-from-uncertain-source_presence', '6-3_ice-cream-truck_presence',
            '7-1_person-or-small-group-talking_presence',
            '7-2_person-or-small-group-shouting_presence',
            '7-3_large-crowd_presence', '7-4_amplified-speech_presence',
            '7-X_other-unknown-human-voice_presence',
            '8-1_dog-barking-whining_presence',
            '1-1_small-sounding-engine_proximity',
            '1-2_medium-sounding-engine_proximity',
            '1-3_large-sounding-engine_proximity',
            '1-X_engine-of-uncertain-size_proximity', '2-1_rock-drill_proximity',
            '2-2_jackhammer_proximity', '2-3_hoe-ram_proximity',
            '2-4_pile-driver_proximity',
            '2-X_other-unknown-impact-machinery_proximity',
            '3-1_non-machinery-impact_proximity', '4-1_chainsaw_proximity',
            '4-2_small-medium-rotating-saw_proximity',
            '4-3_large-rotating-saw_proximity',
            '4-X_other-unknown-powered-saw_proximity', '5-1_car-horn_proximity',
            '5-2_car-alarm_proximity', '5-3_siren_proximity',
            '5-4_reverse-beeper_proximity',
            '5-X_other-unknown-alert-signal_proximity',
            '6-1_stationary-music_proximity', '6-2_mobile-music_proximity',
            '6-3_ice-cream-truck_proximity',
            '6-X_music-from-uncertain-source_proximity',
            '7-1_person-or-small-group-talking_proximity',
            '7-2_person-or-small-group-shouting_proximity',
            '7-3_large-crowd_proximity', '7-4_amplified-speech_proximity',
            '7-X_other-unknown-human-voice_proximity',
            '8-1_dog-barking-whining_proximity', '1_engine_presence',
            '2_machinery-impact_presence', '3_non-machinery-impact_presence',
            '4_powered-saw_presence', '5_alert-signal_presence', '6_music_presence', '7_human-voice_presence',
            '8_dog_presence']
    col2 = classes
    col3 = [x for x in col1 if x not in col2]
    df = pd.read_csv(csv)
    df = df.drop(columns=col3).groupby(
        ['split', 'sensor_id', 'audio_filename', 'borough',
         'block', 'latitude', 'longitude', 'year', 'week', 'day', 'hour']).sum() > 0
    df = df.reset_index()
    df['borough'] = df['borough'].replace(1, 'Manhattan')
    df['borough'] = df['borough'].replace(3, 'Brooklyn')
    df['borough'] = df['borough'].replace(4, 'Queens')

    if main_class is None:
        return df
    else:
        newdf = df[df[main_class] == True]
        return newdf


def create_geodata_frame(df, print_head=False):
    """
    creates a geo data frame that can be used with other functions to do geospatial analysis

    Parameters
    ----------
    df (dataframe): dataframe with 'latitude' and 'longitude' columns (must be named that)
    print (bool) (default: None) : boolean value to specify whether or not to print head

    Returns
    -------
    a geodata frame that has geometry and specifies longitude/latitude points
    works well with heatmap function

    """
    gdf = gpd.GeoDataFrame(
        df, crs={'init': 'epsg:4326'},
        geometry=gpd.points_from_xy(df.longitude, df.latitude))
    if print_head:
        gdf.head()
        return gdf
    else:
        return gdf


def sensor_to_class_gdf(df, main_class, print_head=False):
    """
    This function works specifically well with clustermap because it provides a dataframe that is grouped by sensor and
    mapped to a certain class.

    Parameters
    ----------
    df (dataframe): dataframe
    main_class (string): name of class/column that you want to specifically map sensors to
    print_head (bool) (default:None): specify whether or not to print the head of new gdf

    Returns
    -------
    a geodata frame (with geometry on latitude and longitude) that works well with clustermap

    """
    # create dataframe that is grouped by sensor and counts occurrence of overarching class for each one

    gdf = df.groupby(['sensor_id', 'latitude', 'longitude'])[main_class].count().reset_index()

    # convert to geo dataframe and create geometry column with lat/long
    gdf = gpd.GeoDataFrame(
        gdf, crs={'init': 'epsg:4326'}, geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude))

    if print_head:
        gdf.head()
        return gdf
    else:
        return gdf


def heatmap(gdf, location, gradient=None):
    """
    This is a function that creates a heatmap.
    Parameters
    ----------
    gdf (geodata frame) : geodata frame
    location (list): latitude and longitude  of central map location (e.g. NYC = [40.693943, -74.025])
    gradient (dict) (default:None): option to change the gradient, useful when combining other heatmaps

    Returns
    -------
    a heatmap of where a specific class of data is concentrated by sensor
    """

    emptymap = Map(location=location, zoom_start=12)

    if gradient is not None:
        # create heatmap
        hm = HeatMap(
            list(zip(gdf.latitude.values, gdf.longitude.values)),
            min_opacity=0.2,
            radius=10,
            blur=13,
            gradient=gradient,
            max_zoom=1,
        )
    else:
        # create heatmap
        hm = HeatMap(
            list(zip(gdf.latitude.values, gdf.longitude.values)),
            min_opacity=0.2,
            radius=10,
            blur=13,
            max_zoom=1,
        )

    # add heatmap layer to empty layer
    emptymap.add_child(hm)
    return emptymap


def add_heatmap(original_map, gdf, gradient):
    """
    This function allows you to add a heatmap layer of perhaps data from a different class that you want to compare

    Parameters
    ----------
    original_map (map variable): This must be an existing heatmap, or even an empty map
    gdf (geodata frame): geodata frame
    gradient (dictionary): specifies gradient color configuration so that colors are differentiable
    (e.g. {0.4: ‘blue’, 0.65: ‘lime’, 1: ‘red’})

    Returns
    -------
    A map with an added heatmap layer

    """
    hm = HeatMap(
        list(zip(gdf.latitude.values, gdf.longitude.values)),
        min_opacity=0.2,
        radius=10,
        blur=13,
        gradient=gradient,
        max_zoom=1,
    )
    original_map.add_child(hm)
    return original_map


def clustermap(gdf, location, lat, long):
    """
    This is a function that creates a cluster map.

    Parameters
    ----------
    gdf (geodata frame): geodata frame
    location (list): latitude and longitude  of central map location (e.g. NYC = [40.693943, -74.025])
    lat (string) : dataset's column name for latitude
    long (string) : dataset's column name for longitude

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


def occurrence_by_borough(df):
    """
    plot a pie chart of occurrence by borough

    Parameters
    ----------
    df (dataframe) : dataframe

    Returns
    -------
    a pie chart with occurrence of class in each borough

    """
    # find and tally occurrences in each borough
    borough_freq = df['borough'].value_counts()

    my_colors = ['lightcoral', 'moccasin', 'lightcyan']
    borough_freq.plot.pie(autopct='%1.1f%%', colors=my_colors)
    plt.title('Frequency of Music In Boroughs')
    plt.axis('equal')
    plt.figure(figsize=(2880, 288))
    return plt.show()


def occurrence_by_time(df, time, title = None):
    """
    temporal view of sample data

    Parameters
    ----------
    df (dataframe): dataframe
    time (string): specifies what scope you want to look at (e.g. hour, day, week, year)
    title (string, default:None): option to add a class specific title
    Returns
    -------
    returns a barplot based on what temporal measure you desire to use
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(15, 15))
    if time == 'year':
        plt.title( title + ' occurrence by year')
        return sns.countplot(x='year', data=df)
    elif time == 'week':
        plt.title( title + ' occurrence by week')
        return sns.countplot(x='week', data=df)
    elif time == 'day':
        plt.title( title + ' occurrence by day)
        return sns.countplot(x='week', data=df)
    elif time == 'hour':
        plt.title( title + ' occurrence by hour')
        return sns.countplot(x='hour', data=df)


def occurrence_by_sensor(df, column):
    """
    mapping sensors to data barplot

    Parameters
    ----------
    df (dataframe): dataframe
    column (string): specify

    Returns
    -------
    a barplot that shows samples per sensor

    """
    col = str(column)
    plt.figure(figsize=(20, 20))
    plt.xlabel('Sensor')
    plt.ylabel('Music Presence Occurrence')
    return df.groupby('sensor_id')[col].count().plot.bar()
