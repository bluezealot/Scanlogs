# scan logs , calculate restart time, and start work time.
# Specify the folder path
import os
import re
import ScanInspection as si
import datetime

class log_data:
    content : str
    is_start: bool
    datetime: str
    spend_time: str
    def __init__(self, pcontent = None, pisstart = None, pdatetime = None, pspendtime = None):
        self.datetime = pdatetime
        self.is_start = pisstart
        self.content = pcontent
        self.spend_time = pspendtime

    def to_csv(self):
        result = ''
        if self.datetime is not None:
            result += "\"" + self.datetime.split(" ")[0].replace("\"", "\"\"")
            result += "\",\"" + self.datetime.split(" ")[1].replace("\"", "\"\"")
        if self.is_start is not None:
            if self.is_start:
                result += "\",\"" + "Start"
            else :
                result += "\",\"" + "End"
        if self.spend_time is not None:
            result += "\",\"" + self.spend_time.replace("\"", "\"\"")
        if self.content is not None:
            result += "\",\"" + self.content.replace("\"", "\"\"").replace("\n", "")
        result += "\""
        result += "\n"
        return result

folder_path = '/Volumes/Seagate/work/robot/logs/meitetu/'
datetime_pattern = r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\b'
with open("output_StartWork.csv", "w") as file_out:
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.log') and file_name.startswith('Robot_info'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file_read:
                power_on = True
                line = file_read.readline()
                start_time = ''
                first_line_time = ''
                while line:
                    matches = re.findall(datetime_pattern, line)
                    if not first_line_time:
                        if len(matches) > 0:
                            first_line_time = matches[0]
                    # power on
                    if line.__contains__('initialize persister manager') and not start_time:
                        start_time = matches[0]
                        odata = log_data(line, True, matches[0], str(0))
                        power_on = True
                        file_out.write(odata.to_csv())
                    if line.__contains__('Start navigate to') and power_on:
                        if not start_time:
                            start_time = first_line_time
                        time_span = si.caluclate_timespan(start_time, matches[0])
                        seconds = time_span.total_seconds()
                        odata = log_data(line, False, matches[0], str(seconds))
                        power_on = False
                        start_time = ''
                        file_out.write(odata.to_csv())
                    line = file_read.readline()