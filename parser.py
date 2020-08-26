import pandas as pd
import re

def nextNotDate(s):
    pattern = '^(([0-9)|((1)[0-2]))(\/)([0-9]|[1-3][0-9])(\/)(\d{2}|\d{4}), ([0-9][0-9]|[0-9]):([0-9][0-9])'
    result = re.match(pattern, s)
    if result:
        return False
    return True

def parse_file(text_file):
    '''Convert WhatsApp chat log text file to a Pandas dataframe.'''
    
    with open(text_file, 'r', encoding="utf-8") as f:
        line = f.readline()
        sender = []; message = []; datetime = []
        messageText = ""
        while line:
          print(line)
          # timestamp is before the first dash
          datetime.append(line.split(' - ')[0])

          # sender is between am/pm, dash and colon
          try:
              s = re.search('M - (.*?):', line).group(1)
              sender.append(s)
          except:
              sender.append('')

          # message content is after the first colon
          try:
            messageText += line.split(': ', 1)[1]
            line = f.readline()
            if nextNotDate(line):
              while nextNotDate(line) and line:
                messageText += line
                line = f.readline()   
            message.append(messageText.replace("\n", " "))
            messageText = ""
          except:
            message.append('')
            line = f.readline() 


    df = pd.DataFrame(zip(datetime, sender, message), columns=['timestamp', 'sender', 'message'])
    df['timestamp'] = pd.to_datetime(df.timestamp, format='%m/%d/%Y, %I:%M %p', infer_datetime_format=True)

    # remove events not associated with a sender
    df = df[df.sender != ''].reset_index(drop=True)
    
    return df


