
import re


input_file = open("tess1.txt", "r", encoding='utf-8')
lines = input_file.read().splitlines()
emoji_messages = 0
media_count = 0
total_emoji = 0
total_emoticons = 0
total_emote = 0
emoticons = [':)', ':(', ':|', ":/", ';)']

for line in lines:
    i = 0
    for item in emoticons:
        if item in line:
            total_emoticons = total_emoticons+1
            if i < 1:
                total_emote = total_emote+1
                i = 2


for line in lines:
    emoticons = re.finditer(u'[\U0001f600-\U0001f650]', line)
    count = sum(1 for _ in emoticons)
    if count > 0:
        emoji_messages = emoji_messages+1
    total_emoji = total_emoji+count

print("total emoji  " + str(total_emoji))
print("emoji msg  " + str(emoji_messages))
print("total emote  " + str(total_emoticons))
print("emote msg  " + str(total_emote))
