
# import the data from the csv files into pandas dataframes (data/SpotGenTrack)
df_albums = pd.read_csv('data/SpotGenTrack/DataSources/spotify_albums.csv')
df_artists = pd.read_csv('data/SpotGenTrack/DataSources/spotify_artists.csv')
df_tracks = pd.read_csv('data/SpotGenTrack/DataSources/spotify_tracks.csv')
# FeaturesExtracted from the audio files
df_features = pd.read_csv('data/SpotGenTrack/FeaturesExtracted/lyrics_features.csv')
df_lowlevelaudio = pd.read_csv('data/SpotGenTrack/FeaturesExtracted/low_level_audio_features.csv')
