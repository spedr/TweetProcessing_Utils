import ijson
import unidecode
import re
from datetime import datetime

#file path for stopwords and json exports
stopwords_file_path = 'stopwords.txt'
json_export_file_path = 'the_voice_final.json'

#read files
with open(stopwords_file_path) as f:
    stopwords = f.read().splitlines()

with open(json_export_file_path, 'r') as f:
    objects = ijson.items(f, 'item')
    items = list(objects)

#taken from https://stackoverflow.com/a/49146722
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


#taken from https://gist.github.com/glenbot/4684356
def sanitize_3(user_input, stop_words):
    """Sanitize using standard lists"""
    new_list = []
    for w in user_input:
        if w not in stop_words:
            new_list.append(w)
    return new_list


#remove accents, emoji, convert to all lowercase
for idx, item in enumerate(items):
    items[idx]['text'] = remove_emoji(items[idx]['text'])
    items[idx]['text'] = unidecode.unidecode(items[idx]['text'])
    items[idx]['text'] = items[idx]['text'].lower()
    #print items[idx]['text']


#removing stopwords
#convert every tweet into a list of words
#call sanitize_3 for every list of words
current_string = ''
placeholder_list = [None] * len(items)
master_word_list = []
master_hashtag_list = []
master_user_list = []

for idx, item in enumerate(items):
    #word_list = re.sub("[^\w]", " ", items[idx]['text']).split()
    word_list = re.sub(r'[.!,;:?]', ' ', items[idx]['text']).split()
    word_list = sanitize_3(word_list, stopwords)
    for idx2, word in enumerate(word_list):
        if word_list[idx2][:1] == '#':
            current_string += ' ' + word_list[idx2]
            master_hashtag_list.append(word_list[idx2])
        elif word_list[idx2][:1] == '@':
            current_string += ' ' + word_list[idx2]
            master_user_list.append(word_list[idx2])
        elif word_list[idx2][:3] == '//t':              #dirty workaround
            pass
        elif 'co/' not in word_list[idx2]:
            current_string += ' ' + word_list[idx2]
            master_word_list.append(word_list[idx2])
    placeholder_list[idx] = current_string
    current_string = ''


#release memory immediately
del placeholder_list[:]

#rank words
#adapted from https://github.com/kevinschaul/Word-Rank/blob/master/wordRank.py
l = {}
hashtag_dict = {}
user_dict = {}

for word in master_word_list:
    # if word is in dictionary, increment the value
    # otherwise add the word to dictionary with value 1
    if word in l:
        l[word] += 1
    else:
        l[word] = 1

for hashtag in master_hashtag_list:
    if hashtag in hashtag_dict:
        hashtag_dict[hashtag] += 1
    else:
        hashtag_dict[hashtag] = 1

for user in master_user_list:
    if user in user_dict:
        user_dict[user] += 1
    else:
        user_dict[user] = 1

# this prints the dict out sorted by value in descending order
print '\n#########   Printing ranking of words   #########\n'
for key, value in sorted(l.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
    if value > 300:
        print '%s: %s' % (key, value)

print '\n#########   Printing ranking of hashtags   #########\n'
for key, value in sorted(hashtag_dict.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
        if value > 30:
            print '%s: %s' % (key, value)

print '\n#########   Printing ranking of most mentioned users   #########\n'
for key, value in sorted(user_dict.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
        if value > 200:
            print '%s: %s' % (key, value)

most_retweeted_list = []
list_is_full = False

for tweet in items:
    if 'rt @' in tweet['text']:
        pass
    elif tweet['retweet_count'] > 24:
        most_retweeted_list.append(tweet)

count = 0
print '\n#########   Printing most retweeted tweets   #########\n'
for tweet in sorted(most_retweeted_list, key = lambda x: x['retweet_count'], reverse=True):
    print '@' + tweet['screen_name']
    print tweet['text']
    print 'Retweeted: ' , tweet['retweet_count']
    print '\n'
    if count == 30:
        break
    count+=1

hour_list = []
count = 0
for tweet in items:
    current_date = datetime.strptime(tweet['created_at'],'%Y-%m-%dT%H:%M:%SZ')
    hour_list.append(current_date.hour)

hour_dict = {}


for hour in hour_list:
    if hour in hour_dict:
        hour_dict[hour] += 1
    else:
        hour_dict[hour] = 1

hour_minute_list = []
for tweet in items:
    current_date = datetime.strptime(tweet['created_at'],'%Y-%m-%dT%H:%M:%SZ')

    if int(str(current_date.minute)[:1]) >= 6:
        string = str(current_date.hour) + ':' + '00'
    elif int(str(current_date.minute)[:1]) < 6 and current_date.minute < 10:
        string = str(current_date.hour) + ':' + '00'
    else:
        string = str(current_date.hour) + ':' + str(current_date.minute)[:1] + '0'
    hour_minute_list.append(string)

hour_minute_dict = {}

for hour_minute in hour_minute_list:
    if hour_minute in hour_minute_dict:
        hour_minute_dict[hour_minute] += 1
    else:
        hour_minute_dict[hour_minute] = 1



#going to break on cases that go from 23 to midnight or backwards
print '\n#########   Printing hourly traffic   #########\n'
for key, value in sorted(hour_dict.iteritems(), reverse=True, key=lambda (k,v): (k,v)):
    print '%s: %s' % (key-3, value)

print '\n#########   Printing extended hourly traffic   #########\n'
for key, value in sorted(hour_minute_dict.iteritems(), reverse=True, key=lambda (k,v): (int(k.replace(':', '')),v)):
    print '%s: %s' % (str(int(key[:2])-3) + ':' + key[3] + key[4], value)

print '\n\n'
