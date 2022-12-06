# Data Cleaning and Preprocessing for Modeling

# Functions

# Importing the Data

```python
top_authors_ocd.head(2)```

```python
top_authors_autism.head(2)```

```python
# are there any authors that are in both dataframes?
print(f'Number of authors that are in both dataframes: {len(set(top_authors_ocd.index).intersection(set(top_authors_autism.index)))}')
list_of_cross_posters = list(set(top_authors_ocd.index).intersection(set(top_authors_autism.index)))
print(f'List of authors that are in both dataframes: {list_of_cross_posters}')```

```python
# drop author_flair_type and author_fullname columns from both dataframes
df_ocd = df_ocd.drop(columns=['author_flair_type', 'author_fullname'])
df_autism = df_autism.drop(columns=['author_flair_type', 'author_fullname'])
# combine the title and self text columns into one column with the format `title - selftext`
df_ocd['title_selftext'] = df_ocd.title + ' - ' + df_ocd.selftext
df_autism['title_selftext'] = df_autism.title + ' - ' + df_autism.selftext
# drop the title and selftext columns
df_ocd = df_ocd.drop(columns=['title', 'selftext'])
df_autism = df_autism.drop(columns=['title', 'selftext'])

# rename the `title_selftext` column to `selftext`
df_ocd = df_ocd.rename(columns={'title_selftext': 'selftext'})
df_autism = df_autism.rename(columns={'title_selftext': 'selftext'})

cancel_words = [' ocd ',' aut*','autism','obsess*','compuls*','disorder','executive dysfunction','adhd','diagnosis','ive been taking','spectrum','intrusive thoughts','germaphobes','depression']

# remove punctuation
df_ocd['selftext'] = df_ocd['selftext'].str.replace('[^\w\s]','')
# remove numbers
df_ocd['selftext'] = df_ocd['selftext'].str.replace('\d+', '')
# remove whitespace
df_ocd['selftext'] = df_ocd['selftext'].str.replace('\s+', ' ')

# do the same for the autism dataframe
df_autism['selftext'] = df_autism['selftext'].apply(censor_words)
# remove punctuation
df_autism['selftext'] = df_autism['selftext'].str.replace('[^\w\s]','')
# remove numbers
df_autism['selftext'] = df_autism['selftext'].str.replace('\d+', '')
# remove whitespace
df_autism['selftext'] = df_autism['selftext'].str.replace('\s+', ' ')

# remove words from posts that are in the cancel_words list. There are regex patterns in the cancel_words list so we need to use the `regex=True` parameter

# then remove double spaces
df_ocd['selftext'] = df_ocd['selftext'].str.replace('  ', ' ')
df_autism['selftext'] = df_autism['selftext'].str.replace('  ', ' ')

# make a new dataframe called df_reddit that combines the two dataframes

```

# Sample Posts

```python
# randomly sample one post from each dataframe and print it
print(f'Random OCD post: {df_ocd.sample(1).selftext.values[0]}')
print('='*100)
print(f'Random Autism post: {df_autism.sample(1).selftext.values[0]}')
```

Let's take a look at some of the posts in our dataset after we have applied our censoring function.
They should be free of any words that relate to OCD or Autism such as "OCD" or "Autism", "High Functioning", etc. Terms like "Depression" and "Anxiety" are still present as they are not necessarily related to OCD or Autism and could present as comorbidities.

```python
# randomly sample one post from each dataframe and print it
print(f'Random OCD post: {df_ocd.sample(1).selftext.values[0]}')
print('='*100)
print(f'Random Autism post: {df_autism.sample(1).selftext.values[0]}')
```

## Equilibrium 

```python
df_reddit = pd.DataFrame(columns=df_ocd.columns)
# what is the length of the shorter dataframe?
if len(df_ocd) < len(df_autism): # if the OCD dataframe is shorter
    shorter_df = df_ocd # set the shorter dataframe to the OCD dataframe
    longer_df = df_autism # set the longer dataframe to the Autism dataframe
else: # if the Autism dataframe is shorter
    shorter_df = df_autism
    longer_df = df_ocd

# add the shorter dataframe to the new dataframe using concat
df_reddit = pd.concat([df_reddit, shorter_df], axis=0)
# shorten the longer dataframe to the length of the shorter dataframe
longer_df = longer_df.head(len(shorter_df))
# add the shortened longer dataframe to the new dataframe using concat
df_reddit = pd.concat([df_reddit, longer_df], axis=0)

# reset the index
df_reddit = df_reddit.reset_index(drop=True)


# shuffle the dataframe
df_reddit = df_reddit.sample(frac=1).reset_index(drop=True)
# check the dimensions of the new dataframe
print(f'Dimensions of the new dataframe: {df_reddit.shape}')
df_reddit.head(5)```

```python
# double check that the number of posts for each subreddit is the same
print(f'Number of posts for OCD: {len(df_reddit[df_reddit.target == 1])}')
print(f'Number of posts for Autism: {len(df_reddit[df_reddit.target == 0])}')
```

```python
df_ocd.head(2)```

```python
df_autism.head(2)```

```python
# find any of the medications in the selftext column that are in the data/drug_info.csv file under the Medication Name column and replace them with ' ' (empty string)
drug_info = pd.read_csv('../data/drug_info.csv')
drug_info['Medication Name'] = drug_info['Medication Name'].str.lower()
# create a list of the medications
medications = drug_info['Medication Name'].tolist()
print(f'Number of medications: {len(medications)}')
# how many posts contain a medication?
print(f'Number of posts that contain a medication: {len(df_reddit[df_reddit.selftext.str.contains("|".join(medications), regex=True)])}')```

```python
medications[0]```

```python
medications = [med for med in medications if len(med) > 5]
# create a list of rows and the medications mentioned in each row
import os
medications_mentioned = []
if os.path.exists('../data/cleaned_reddit.csv'):
    pass
else:
    # with alive_bar (len(df_reddit)) as bar:
    for index, row in df_reddit.iterrows(): # iterate through each row in the dataframe
        # use regex to find all of the medications in the selftext column
        meds = re.findall(r'\b(?:{})\b'.format('|'.join(medications)), row['selftext'])
        if len(meds) > 0: # if there are medications mentioned in the post
            # replace the medications with ' ' (empty string)
            row['selftext'] = re.sub(r'\b(?:{})\b'.format('|'.join(medications)), ' ', row['selftext'])
            medications_mentioned.extend(meds) # add the medications to the medications_mentioned list
            # remove duplicate medications
            medications_mentioned = list(set(medications_mentioned))
            # bar()
# remove the words from the selftext column that are in the medications list
# if the file does not already exist, create it
if os.path.exists('../data/cleaned_reddit.csv'):
    # load the file
    df_reddit = pd.read_csv('../data/cleaned_reddit.csv')
else:
    print('File does not exist. Creating it now. Before meds removed from selftext the length of the dataframe is: ', len(df_reddit))
    print(f' Removed {len(medications_mentioned)} medications from the selftext column')
    # save the dataframe to a csv file
    df_reddit.to_csv('../data/cleaned_reddit.csv', index=False)
# Now we want to clean the text in the self text column
# remove punctuation
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'[^\w\s]','')
# remove numbers
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'\d+', '')
# remove double spaces
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'  ', ' ')
# remove single characters
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'\b\w\b', '').str.replace(r'\s+', ' ')
# remove newlines
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'\n', ' ')
# remove urls
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'http\S+', '')
# remove html tags
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'<.*?>', '')
# remove extra spaces
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'\s+', ' ')
# remove extra spaces at the beginning of the string
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'^\s+', '')
# remove extra spaces at the end of the string
df_reddit['selftext'] = df_reddit['selftext'].str.replace(r'\s+$', '')

# save progress to a csv file
df_reddit.to_csv('../data/cleaned_reddit.csv', index=False)


# read the file into a dataframe
df_reddit = pd.read_csv('../data/cleaned_reddit.csv')
# remove any rows that have a null value in the selftext column
df_reddit = df_reddit.dropna(subset=['selftext'])
# reset the index
df_reddit = df_reddit.reset_index(drop=True)
# check the dimensions of the dataframe
print(f'Dimensions of the dataframe: {df_reddit.shape}')


def num_distinct_words(text,df):
    """
    num_distinct_words takes in a string and a dataframe and returns the number of distinct words in the string

    Parameters

    :param text: string
    :type text: str
    :param df: dataframe
    :type df: pandas.core.frame.DataFrame
    :return: number of distinct words in the string
    :rtype: int
    """
    # for this text, find the words that do not appear in any other text in the dataframe column 'selftext'
    # split the text into a list of words
    if type(text) == str:
        text = text.split(' ')
        # find the number of words that are not in any other text in the dataframe
    else:
        # the text is a list of words
        words = text
        pass
    #words = text.split(' ')
    # find the number of words that are not in any other text in the dataframe
    distinct_words = [word for word in words if word not in df['selftext'].str.split(' ').sum()]
    number_distinct_words = len(distinct_words) # find the number of distinct words
    return number_distinct_words, distinct_words```

```python
df_reddit.head(5)```

```python
df_reddit.isna().sum()```

```python
# save df_reddit to a csv file
print('Saving the dataframe to a csv file')
df_reddit.to_csv('../data/cleaned_reddit_before_dataviz.csv', index=False)```

# Examining UTC range based on data Visualizations


```python
# Load the data
df = pd.read_csv('../data/cleaned_reddit.csv')
try:
    #~ Dropping Constant Value columns from the data ~#
    df.drop(columns=['is_original_content'], inplace=True)
    #~ Dropping duplicated selftext rows from the data ~#
    print(f'Before dropping duplicates, the shape of the data is: {df.shape}')
    preshape = df.shape[0]
    df.drop_duplicates(subset=['selftext'], inplace=True)
    print(f'After dropping duplicates, the shape of the data is: {df.shape}')
    print(f'The number of rows dropped is: {preshape - df.shape[0]}')
except Exception as e:
    print(f'{e} - No duplicates to drop')
# Create a new column that is the length of the selftext
df['selftext_length'] = df['selftext'].str.len()

# Create a new column that is the number of words in the selftext
df['selftext_word_count'] = df['selftext'].str.split().str.len()

# A column for each letter of the alphabet that is the number of times that letter appears in the selftext
for letter in 'abcdefghijklmnopqrstuvwxyz':
    df[f'{letter}'] = df['selftext'].str.count(letter)

# save the data to a csv
df.to_csv('../data/cleaned_reddit.csv', index=False)
df.head()```

```python
# make a figure plotting letters against number of occurances in selftext for each selftext length bin. To avoid the ValueError "ValueError: num must be 1 <= num <= 16, not 17" the number of bins is set to 25 instead of 26 (the number of letters in the alphabet).
# add a space between the plots to make them easier to read and to make the plot more aesthetically pleasing
# for this code block ignore the IndexError

fig, axes = plt.subplots(5, 5, figsize=(20,20), sharey=True, sharex=True)
fig.subplots_adjust(hspace=0.5, wspace=0.5)
# the suptitle should not have so much space between it and the subplots
# the x and y labels should be larger
for i, letter in enumerate('abcdefghijklmnopqrstuvwxyz'):
    try:
        ax = axes[i//5, i%5]
        ax.scatter(df['selftext_length'], df[f'{letter}'], alpha=0.5)
        ax.set_title(letter)
        ax.set_xlabel('Number of Occurances')
        ax.set_ylabel('Selftext Length')
    except IndexError:
        pass
fig.suptitle('Letter Occurances in Selftext by Selftext Length', fontsize=20, y=0.92)
plt.savefig('../images/letter_histograms.png')
plt.show();
```

```python
# if the data/cleaned_reddit_withsentiment.csv file does not exist, run the following code to create it
# use alivebar
from alive_progress import alive_bar

# if the file already exists, skip this code block and load the file
# if the file exists but the length of the rows is not the same as the length of the rows in the cleaned_reddit.csv file, run the following code to create it
if not os.path.exists('../data/cleaned_reddit_withsentiment.csv') or os.path.getsize('../data/cleaned_reddit_withsentiment.csv') != os.path.getsize('../data/cleaned_reddit.csv'):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    # if the file has a sentiment column, then use that value for each row in the sentiment column (we are just missing some rows)
    # for each row in df, get the sentiment value from the sentiment column and add it to the row in the sentiment column for the new dataframe
    # if the sentiment column does not exist, then use the sentiment value from the sentiment_analysis function
    with alive_bar(len(df)) as bar:
        for i, row in df.iterrows():
            try:
                # load compound, pos, neu, neg values from the sentiment columns in df
                compound = row['sentiment']
                pos = row['positive']
                neu = row['neutral']
                neg = row['negative']
            except KeyError:
                compound, pos, neu, neg = analyzer.polarity_scores(row['selftext'])['compound'], analyzer.polarity_scores(row['selftext'])['pos'], analyzer.polarity_scores(row['selftext'])['neu'], analyzer.polarity_scores(row['selftext'])['neg']
            # add the sentiment values to the new dataframe
            df.loc[i, 'sentiment'] = compound
            df.loc[i, 'positive'] = pos
            df.loc[i, 'neutral'] = neu
            df.loc[i, 'negative'] = neg
            
            bar()
    # save the data to a csv
    df.to_csv('../data/cleaned_reddit_withsentiment.csv', index=False)
df.head()
```

# Pairplot

make a pairplot of the sentiment	positive	neutral	negative, words in the post, and length of the post to see if there are any correlations between these variables.

This graphic has several interesting key elements.

We now have several columns that we don't want to interfere with the analysis as they could be considered "leaks" of information. We will drop these columns and save the data to a new csv file.
These are: 
1. `author`
2. `created_utc`



# data

* [X_df.csv](./data/X_df.csv) - The features used in the model.
* [autism_thread.csv](./data/autism_thread.csv) - The raw data from the autism thread.
* [best_scores.csv](./data/best_scores.csv) - The best scores from the model.
* [cleaned_reddit.csv](./data/cleaned_reddit.csv) - The cleaned data from the autism thread.
* [cleaned_reddit_withsentiment.csv](./data/cleaned_reddit_withsentiment.csv) - The cleaned data from the autism thread with sentiment analysis. Also includes the OCD thread.
* [cvec.csv](./data/cvec.csv) - The cvec data. Count Vectorized data. This is used in the model.
* [cvec_vocab.txt](./data/cvec_vocab.txt) - The vocabulary used in the cvec data.
* [df_after_feature_engineering.csv](./data/df_after_feature_engineering.csv) - The data after feature engineering. This may not be used in the model.
* [df_cleaned.csv](./data/df_cleaned.csv) - The cleaned data from the autism and OCD threads.
* [drug_info.csv](./data/drug_info.csv) - The drug information from the drugbank database.
* [global_variables.csv](./data/global_variables.csv) - The global variables used in the model.
* [master_results_dataframe.csv](./data/master_results_dataframe.csv) - The master results dataframe.
* [ocd_thread.csv](./data/ocd_thread.csv) - The raw data from the OCD thread.
* [reddit_threads.csv](./data/reddit_threads.csv) - The raw data from the autism and OCD threads.
* [tfidf.csv](./data/tfidf.csv) - The tfidf data. Term Frequency Inverse Document Frequency data. This is used in the model.
* [tfidf_vocab.txt](./data/tfidf_vocab.txt) - The vocabulary used in the tfidf data.
* [y.csv](./data/y.csv) - The target variable used in the model.

