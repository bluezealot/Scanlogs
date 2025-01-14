import requests
import re
from bs4 import BeautifulSoup
from lxml import etree


class TourSpot:
    spot_name : str
    introduction : str
    category : str
    area : str
    address : str

    def __init__(self, spot_name = None, introduction = None, category = None, area = None, address = None, add_table = None, add_info = None):
        self.spot_name = spot_name
        self.introduction = introduction
        self.category = introduction
        self.area = area
        self.address = address
        self.add_table = add_table
        self.add_info = add_info

    def to_csv(self):
        result = ''
        result += "\"" + self.spot_name.replace("\"", "\"\"")
        result += "\",\"" + self.introduction.replace("\"", "\"\"")
        result += "\",\"" + self.category.replace("\"", "\"\"")
        if self.area is not None:
            result += "\",\"" + self.area.replace("\"", "\"\"")
        else:
            result += "\",\"" + ' '
        if self.address is not None:
            result += "\",\"" + self.address.replace("\"", "\"\"")
        else:
            result += "\",\"" + ' '
        if self.add_table is not None:
            result += "\",\"" + self.add_table.replace("\"", "\"\"")
        else:
            result += "\",\"" + ' '
        if self.add_info is not None:
            result += "\",\"" + self.add_info.replace("\"", "\"\"")
        else:
            result += "\",\"" + ' '
        result += "\""
        result += "\n"
        return result


def convert_xpath_to_dom(xpath_element):
    lxml_string = etree.tostring(xpath_element, pretty_print=True, encoding='unicode')
    soup_element = BeautifulSoup(lxml_string, 'html.parser')
    return soup_element

def load_spot(url:str):
    result = TourSpot()
    spot_html = requests.get(url)
    lxml_spot_element = etree.HTML(spot_html.text)
    name_element = lxml_spot_element.xpath('/html/body/main/div[2]/div/div[1]/h2')
    result.spot_name = name_element[0].text
    category_element = lxml_spot_element.xpath('/html/body/main/div[3]/div/div[1]/div[2]/div[1]/dl[1]/dd')
    category_dom = convert_xpath_to_dom(category_element[0])
    result.category = category_dom.get_text()
    area_element = lxml_spot_element.xpath('/html/body/main/div[3]/div/div[1]/div[2]/div[1]/dl[2]/dd')
    area_dom = convert_xpath_to_dom(area_element[0])
    result.area = area_dom.get_text()
    address_element = lxml_spot_element.xpath('/html/body/main/div[3]/div/div[1]/div[2]/div[2]/dl/dd')
    if len(address_element) > 0:
        address_dom = convert_xpath_to_dom(address_element[0])
        result.address = address_dom.get_text()
    intro_element = lxml_spot_element.xpath('/html/body/main/div[3]/div/div[2]')
    intro_dom = convert_xpath_to_dom(intro_element[0])
    result.introduction = intro_dom.get_text()
    addinfo_element = lxml_spot_element.xpath('/html/body/main/div[3]/div/div[3]/div')
    if len(addinfo_element) > 0:
        result.add_info = ''
        for addinfo in addinfo_element:
            result.add_info += convert_xpath_to_dom(addinfo).get_text() + '\n'
    addtable_element = lxml_spot_element.xpath('/html/body/main/div[3]/div/table')
    if len(addtable_element) > 0:
        result.add_table = ''
        addtable_dom = convert_xpath_to_dom(addtable_element[0])
        rows = addtable_dom.findAll('tr')
        for row in rows:
            result.add_table += row.get_text()
    return result

base_url = 'https://www.hakone.or.jp'
spot_hp = 'https://www.hakone.or.jp/?p=30&&sctg=%E8%A6%B3%E3%81%9F%E3%81%84&&pg=3&s=40'

spot_hp_response = requests.get(spot_hp)
if spot_hp_response.status_code == 200:
    html_content = spot_hp_response.text
else:
    print(f"Failed to fetch the page. Status code: {spot_hp_response.status_code}")

lxml_hpelement = etree.HTML(spot_hp_response.text)
search_list = lxml_hpelement.xpath('/html/body/main/div[4]/div/div[1]')
search_result_dom = convert_xpath_to_dom(search_list[0])
all_spots = search_result_dom.findAll(attrs={'class': 'spot_idx_box'})
with open("output_spot.csv", "w") as file_out:
    for spot in all_spots:
        atag = spot.findAll('a')
        spot_detail_url = base_url + atag[0]['href']
        print(f'Processing {spot_detail_url}')
        if 'gana=member' in spot_detail_url:
            spot = load_spot(spot_detail_url)
            file_out.write(spot.to_csv())
