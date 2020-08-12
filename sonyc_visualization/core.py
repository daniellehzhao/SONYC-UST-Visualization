import pandas as pd
import seaborn as sns
import matplotlib as plt
import folium
from folium import Map
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap


def clean(csv, classes, main_class=None):
    """
    cleans data by taking out unnecessary columns and only counting occurrences that are true

    Parameters
    ----------
    csv : path or name of csv file (string)
    classes : desired class and subclass column names (list format)
    main_class : name of the working overarching class (string)

    Returns
    -------

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


def heatmap(gdf, location):
    """
    This is a function that creates a heatmap.
    Parameters
    ----------
    gdf : geodata frame
    location : latitude and longitude (in list format) of central map location (e.g. NYC = [40.693943, -74.025])

    Returns
    -------
    a heatmap of where a specific class of data is concentrated by sensor
    """

    emptymap = Map(location=location, zoom_start=12)

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
