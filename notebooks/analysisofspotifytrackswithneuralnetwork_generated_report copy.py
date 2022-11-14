
# import the data from the csv files into pandas dataframes (data/SpotGenTrack)
df_albums = pd.read_csv('data/SpotGenTrack/DataSources/spotify_albums.csv')
df_artists = pd.read_csv('data/SpotGenTrack/DataSources/spotify_artists.csv')
df_tracks = pd.read_csv('data/SpotGenTrack/DataSources/spotify_tracks.csv')
# FeaturesExtracted from the audio files
df_features = pd.read_csv('data/SpotGenTrack/FeaturesExtracted/lyrics_features.csv')
df_lowlevelaudio = pd.read_csv('data/SpotGenTrack/FeaturesExtracted/low_level_audio_features.csv')

# print the columns for each data file to see what data is available
print(f'\ncolumns in the albums file: ',df_albums.columns)
print(f'\ncolumns in the artists file: ',df_artists.columns)
print(f'\ncolumns in the tracks file: ',df_tracks.columns)
print(f'\ncolumns in the features file: ',df_features.columns)
print(f'\ncolumns in the lowlevelaudio file: ',df_lowlevelaudio.columns)



# get the counts of each genre
genre_counts = df_tracks['playlist'].value_counts()



