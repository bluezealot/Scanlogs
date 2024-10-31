import os
import re

class LogEntity:
    datetime: str
    thread: str
    level: str
    class_name: str
    content: str
    def __init__(self, pdatetime = None, pthread = None, plevel = None, pclass_name = None, pcontent = None):
        self.datetime = pdatetime
        self.thread = pthread
        self.level = plevel
        self.class_name = pclass_name
        self.content = pcontent
    def toCsv(self):
        result = ''
        if self.datetime is not None:
            result += "\"" + self.datetime.split(" ")[0].replace("\"", "\"\"")
            result += "\",\"" + self.datetime.split(" ")[1].replace("\"", "\"\"")
        if self.thread is not None:
            result += "\",\"" + self.thread.replace("\"", "\"\"")
        if self.level is not None:
            result += "\",\"" + self.level.replace("\"", "\"\"")
        if self.class_name is not None:
            result += "\",\"" + self.class_name.replace("\"", "\"\"")
        if self.content is not None:
            result += "\",\"" + self.content.replace("\"", "\"\"")
        result += "\""
        return result

# Specify the folder path
folder_path = '/Volumes/Seagate/work/robot/logs/meitetu/'
# Regular expression to match datetime in YYYY-MM-DD HH:MM:SS format
datetime_pattern = r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\b'
robot_pattern = r'\b\.robot\.\b'
thread_pattern = r'\b\[.*\]\b'
speech_pattern = r'\btext=.*, male\b'
content_pair = {}

def scan_line(line:str):
    matches = re.findall(datetime_pattern, line)
    # Get datetime
    if len(matches) > 0:
        datetime = matches[0]
        match_speech = re.findall(speech_pattern, line)
        if len(match_speech) > 0:
            speech_text = match_speech[0]
            speech_text = speech_text.replace("text=", "")
            speech_text = speech_text.replace(", male", "")
            aLog = LogEntity(pdatetime = datetime,pcontent = speech_text)
            if content_pair.__contains__(aLog.content):
                content_pair[aLog.content].append(aLog)
            else:
                log_list = [];
                log_list.append(aLog)
                content_pair[aLog.content] = log_list


# List all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.log') and file_name.startswith('SPEECH'):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            line = file.readline()
            while line:
                print(line.strip())
                scan_line(line)
                line = file.readline()

with open("output.csv", "w") as file:
    for key,log_list in content_pair.items():
        for alog in log_list:
            file.write(alog.toCsv() + '\n')
