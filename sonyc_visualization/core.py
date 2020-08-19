import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import geopandas as gpd
from folium import Map
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap


def load_df(csv, classes=None, main_class=None):
    """
    loads pandas dataframe to work with
    allows you to load the entire dataframe but also allows you to take out unnecessary columns and only counting
    occurrences that are true

    Parameters
    ----------
    csv (string) : path or name of csv file
    classes (list) : desired class and subclass column names. If not specified, the function will load entire dataframe
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
    df = pd.read_csv(csv)

    if classes is not None:
        col2 = classes
        col3 = [x for x in col1 if x not in col2]
        df = df.drop(columns=col3)

    df = df.groupby(
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


def create_geodataframe(df, print_head=False):
    """
    A GeoDataFrame is a pandas.DataFrame that has one GeoSeries column referred to as the GeoDataFrame’s “geometry”.
    When a spatial method is applied (such as trying to create a heatmap) to a GeoDataFrame,commands will always act on
    the “geometry” column.

    Without converting to a GeoDataFrame, it will not be possible to use the other functions to create various maps
    because the latitude and longitude columns do not function separately/on their own for spatial analysis.

    Parameters
    ----------
    df (dataframe): dataframe with 'latitude' and 'longitude' columns (must be named that)
    print (bool) (default: None) : boolean value to specify whether or not to print head

    Returns
    -------
    a GeoDataFrame that has geometry and specifies longitude/latitude points
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


def heatmap(gdf, location, gradient=None):
    """
    This is a function that creates a heatmap.
    Parameters
    ----------
    gdf (geodata frame) : GeoDataFrame
    location (list): latitude and longitude  of central map location (e.g. NYC = [40.693943, -74.025])
    gradient (dict) (default:None): option to change the gradient, useful when combining other heatmaps

    Returns
    -------
    a heatmap of where a specific class of data is _ by sensor
    """

    emptymap = Map(location=location, zoom_start=12)

    # create heatmap
    hm = HeatMap(
        list(zip(gdf.latitude.values, gdf.longitude.values)),
        min_opacity=0.2,
        radius=10,
        blur=13,
        gradient=gradient,
        max_zoom=1,
    )
    # add heatmap layer to empty layer
    emptymap.add_child(hm)
    return emptymap


def add_heatmap(original_map, gdf, gradient=None):
    """
    This function allows you to add a heatmap layer of perhaps data from a different class that you want to compare

    Parameters
    ----------
    original_map (map variable): This must be an existing heatmap, or even an empty map
    gdf (GeoDataFrame): GeoDataFrame
    gradient (dict): specifies gradient color configuration so that colors are differentiable. If value is None, the
    default gradient is {0.4: ‘blue’, 0.65: ‘lime’, 1: ‘red’}

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


def clustermap(df, main_class, location):
    """
    This is a function that creates a cluster map.

    Parameters
    ----------
    df (dataframe): dataframe with latitude and longitude columns
    main_class (string): overarching class to analyze from dataframe
    location (list): latitude and longitude  of central map location (e.g. NYC = [40.693943, -74.025])

    Returns
    -------
    A cluster map of sensors

    """
    if ('latitude' in df.columns) and ('longitude' in df.columns):

        # create dataframe that is grouped by sensor and counts occurrence of overarching class for each one

        gdf = df.groupby(['sensor_id', 'latitude', 'longitude'])[main_class].count().reset_index()

        # convert to geo dataframe and create geometry column with lat/long

        gdf = gpd.GeoDataFrame(
            gdf, crs={'init': 'epsg:4326'}, geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude))

        circlemap = folium.Map(location=location, zoom_start=12)

        # add marker for each sensor, use a clustered view (zoom in to see individual sensors)
        # added labels for each sensor which displays the sensor number and the counted occurence for music
        mc = MarkerCluster()
        for index, row in gdf.iterrows():
            mc.add_child(folium.Marker(location=[str(row['latitude']), str(row['longitude'])],
                                       clustered_marker=True))

        # add marker cluster layer to empty map

        circlemap.add_child(mc)
        return circlemap
    else:
        print("Dataframe does not have latitude and longitude columns or check to make sure column names are 'latitude'"
              "and 'longitude'")


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


def occurrence_by_time(df, time, sound_class):
    """
    temporal view of sample data

    Parameters
    ----------
    df (dataframe): dataframe with only instances where specified class is present/true
    time (string): specifies what scope you want to look at (e.g. hour, day, week, year)
    sound_class (string): specify which class is being analyzed for title of plot
    Returns
    -------
    returns a barplot based on what temporal measure you desire to use
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(15, 15))
    if time in df.columns:
        plt.title('{} occurrence by {}'.format(sound_class, time))
        return sns.countplot(x=time, data=df)
    else:
        print("This column does not exist in given dataframe")


def occurrence_by_sensor(df, class_column, title):
    """
    mapping sensors to data barplot

    Parameters
    ----------
    df (dataframe): dataframe
    class_column (string): specify class column name

    Returns
    -------
    a barplot that shows samples per sensor

    """
    if class_column in df.columns:
        col = str(class_column)
        plt.figure(figsize=(20, 20))
        plt.xlabel('Sensor')
        plt.ylabel(title + ' Presence Occurrence By Sensor')
        return df.groupby('sensor_id')[col].count().plot.bar()
    else:
        print("Class column does not exist in given dataframe")
