import os
import re
from datetime import datetime

class inspection_data:
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

def caluclate_timespan(start_time, end_time):
    datetime_obj1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
    datetime_obj2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    result = datetime_obj2 - datetime_obj1
    return result

with open("output_outInspect.csv", "w") as file_out:
    with open("output_inspect.csv", "w") as file_in:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.log') and file_name.startswith('Robot_info'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file_read:
                    line = file_read.readline()
                    start_time = ''
                    instart_time = ''
                    while line:
                        print(line.strip())
                        spend_time = str(0)
                        inspend_time = str(0)
                        if line.__contains__('OutSideInspectionActivity') and line.__contains__('InspectionActivity onCreate start'):
                            matches = re.findall(datetime_pattern, line)
                            if start_time:
                                time_span = caluclate_timespan(matches[0], start_time)
                                spend_time = str(time_span)
                            start_time = matches[0]
                            odata = inspection_data(line, True, matches[0], spend_time)
                            spend_time = str(0)
                            file_out.write(odata.to_csv())
                        if line.__contains__('OutSideInspectionActivity') and line.__contains__('InspectionActivity stopNav'):
                            matches = re.findall(datetime_pattern, line)
                            if start_time:
                                time_span = caluclate_timespan(matches[0], start_time)
                                spend_time = str(time_span)
                            odata = inspection_data(line, False, matches[0], spend_time)
                            start_time = ''
                            spend_time = str(0)
                            file_out.write(odata.to_csv())
                        if line.__contains__('InspectionActivity') and line.__contains__('InspectionActivity onCreate start'):
                            matches = re.findall(datetime_pattern, line)
                            if instart_time:
                                time_span = caluclate_timespan(matches[0], instart_time)
                                inspend_time = str(time_span)
                            instart_time = matches[0]
                            odata = inspection_data(line, True, matches[0], inspend_time)
                            inspend_time = str(0)
                            file_in.write(odata.to_csv())
                        if line.__contains__('InspectionActivity') and line.__contains__('InspectionActivity stopNav'):
                            matches = re.findall(datetime_pattern, line)
                            if instart_time:
                                time_span = caluclate_timespan(matches[0], instart_time)
                                spend_time = str(time_span)
                            odata = inspection_data(line, False, matches[0], inspend_time)
                            instart_time = ''
                            inspend_time = str(0)
                            file_in.write(odata.to_csv())
                        line = file_read.readline()