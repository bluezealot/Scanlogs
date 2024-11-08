import requests
import base64
import os

# Define the URL
url = "http://15.168.2.6:24397/database/redis/get_db_keylist"

# Define headers
headers = {
    "x-http-token": "kt4yBdBgB1holsn9A7IqkJDMGqg79TBFwaHXExTtett26HND",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Cookie": "http_order=id%20desc; http_serverType=nginx; http_bt_user_info=%7B%22status%22%3Atrue%2C%22msg%22%3A%22%E8%8E%B7%E5%8F%96%E6%88%90%E5%8A%9F!%22%2C%22data%22%3A%7B%22username%22%3A%22185****0805%22%7D%7D; http_pro_end=-1; http_ltd_end=-1; http_rank=list; http_file_recycle_status=true; http_Path=%2F; a226b7e8358d3341c162c1c7f71f079a=8592a007-2fc7-44c2-bda1-dd2e4a5d20b5.nJeDZBAaDZf1K1qv9nK_GaCH1Qs"
}

# Define query parameters
params = {
    "param1": "value1",
    "param2": "value2"
}

# Define the JSON payload
payload = {
    "data": '{"limit":20,"db_idx":1,"search":"","sid":0,"p":No}',
}
template = '{"limit":20,"db_idx":1,"search":"","sid":0,"p":No}'

for round in range(3):
    for i in range(23):
        payload['data'] = template.replace('No', str(i))
        print('Page info:', payload['data'])
        # Make the POST request
        response = requests.post(url, headers=headers, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Print the response content
            print("Response JSON")
            for adata in response.json()["data"]:
                if adata['name'] and adata['val']:
                    if adata['val'].__contains__('photo'):
                        val = adata['name'].strip('\"')
                        val = val.replace('GamePrize:', '').replace('GameScore:', '')
                        request_url = 'http://15.168.2.6:81/prod-api/robot/game/prize/' + val
                        print('requesting', val)
                        response_image = requests.post(request_url)
                        if not response_image.json()['data']:
                            print('Can not get photo:', response_image.json())
                        base64_string = response_image.json()['data']['score']['photo']
                        image_data = base64.b64decode(base64_string)
                        output_path = "image_folder/" + val + ".jpg"
                        if os.path.exists(output_path):
                            print('Round ', str(round) + ' Image exists')
                        else:
                            print('Round ', str(round) + " Writing:", output_path)
                            with open(output_path, "wb") as image_file:
                                image_file.write(image_data)
        else:
            print("Request failed with status code:", response.status_code)
