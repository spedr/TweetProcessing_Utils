import ijson
import unidecode
import re

#file path for stopwords and json exports
stopwords_file_path = 'stopwords.txt'
json_export_file_path = 'lula.json'

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
    #print items[count]['text']


#removing stopwords
#convert every tweet into a list of words
#call sanitize_3 for every list of words
current_string = ''
master_string = ''
placeholder_list = [None] * len(items)

for idx, item in enumerate(items):
    word_list = re.sub("[^\w]", " ", items[idx]['text']).split()
    word_list = sanitize_3(word_list, stopwords)
    for idx2, word in enumerate(word_list):
        current_string += ' ' + word_list[idx2]
    placeholder_list[idx] = current_string
    current_string = ''


for idx, item in enumerate(items):
    items[idx]['text'] = placeholder_list[idx]
    master_string += ' ' + placeholder_list[idx]
    #print items[idx]['text']


#rank words
#adapted from https://github.com/kevinschaul/Word-Rank/blob/master/wordRank.py
l = {}

for word in master_string.split():
    # if word is in dictionary, increment the value
    # otherwise add the word to dictionary with value 1
    if word in l:
        l[word] += 1
    else:
        l[word] = 1

# this prints the dict out sorted by value in descending order
for key, value in sorted(l.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
    if value > 19:
        print '%s: %s' % (key, value)
