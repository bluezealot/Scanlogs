import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

shop_hp = 'https://www.harune-odawara.com/shop-guide'

shop_hp_response = requests.get(shop_hp)
if shop_hp_response.status_code == 200:
    html_content = shop_hp_response.text
else:
    print(f"Failed to fetch the page. Status code: {shop_hp_response.status_code}")

soup_data = BeautifulSoup(html_content, 'html.parser')
# Matches IDs like 'unit-3757', 'unit-3758'
pattern = re.compile(r'^extSubTt.*$')
# Find all elements with matching IDs
matching_elements = soup_data.find_all(attrs={'id': pattern})
# Check if each element contains a specific class (e.g., 'hsNormal')
content_pair = {}
class shopInfo:
    category : str
    enCategory : str
    shop_name : str
    introduction : str
    main_product : str
    telephone : str
    op_time : str
    url : str
    def to_csv(self):
        result = ''
        result += "\"" + self.category.replace("\"", "\"\"")
        result += "\",\"" + self.enCategory.replace("\"", "\"\"")
        result += "\",\"" + self.shop_name.replace("\"", "\"\"")
        result += "\",\"" + self.introduction.replace("\"", "\"\"")
        result += "\",\"" + self.main_product.replace("\"", "\"\"")
        result += "\",\"" + self.telephone.replace("\"", "\"\"")
        result += "\",\"" + self.op_time.replace("\"", "\"\"")
        result += "\",\"" + self.url.replace("\"", "\"\"")
        result += "\""
        result += "\n"
        return result
def get_text_from_xpath(xpath_element):
    lxml_string = etree.tostring(xpath_element, pretty_print=True, encoding='unicode')
    soup_element = BeautifulSoup(lxml_string, 'html.parser')
    result = soup_element.get_text()
    return result

def get_tabledata_from_xpath(xpath_element, ashop : shopInfo):
    lxml_string = etree.tostring(xpath_element, pretty_print=True, encoding='unicode')
    soup_element = BeautifulSoup(lxml_string, 'html.parser')
    ashop.main_product = soup_element.findAll('tr')[0].find_all()[1].get_text()
    ashop.telephone = soup_element.findAll('tr')[1].find_all()[1].get_text()
    ashop.op_time = soup_element.findAll('tr')[2].find_all()[1].get_text()

def load_shop(link:str, ashop : shopInfo):
    a_shop_page = requests.get(link)
    lxml_element = etree.HTML(a_shop_page.text)
    name_element = lxml_element.xpath('/html/body/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[1]/div/div/div/h3')
    ashop.shop_name = name_element[0].text
    description_element = lxml_element.xpath('/html/body/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div')
    if len(description_element) == 0:
        description_element = lxml_element.xpath(
            '/html/body/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div[2]/div/div/div')
    ashop.introduction = get_text_from_xpath(description_element[0])
    table_element = lxml_element.xpath(
        '/html/body/div[1]/div/div[3]/div/div/div/div/div[5]/div/div/div[1]/div/div/div/table')
    if len(table_element) == 0:
        table_element = lxml_element.xpath(
            '/html/body/div[1]/div/div[3]/div/div/div/div/div[4]/div/div/div[1]/div/div/div/table')
    get_tabledata_from_xpath(table_element[0], ashop)

with open("output_shop_guide.csv", "w") as file_out:
    for element in matching_elements:
        classes = element.get('class', [])
        if 'extSubTtl' in classes:## Shop category title.
            contents = element.find().contents
            strCategory = contents[0]
            enCategory = contents[2].get_text()
            p_shop = re.compile(r'^extCatList4_item_.*$')
            matching_shops = element.parent.fetchNextSiblings()[0].find_all(attrs={'id' : p_shop})
            for e_shop in matching_shops:
                aShop = shopInfo()
                link_element = e_shop.find_all(attrs={'class' : 'extCatList4Link'})
                strLink = link_element[0].find('a')['href']
                print(f"Href: {strLink}")
                aShop.url = strLink
                aShop.category = strCategory
                aShop.enCategory = enCategory
                load_shop(strLink, aShop)
                file_out.write(aShop.to_csv())

