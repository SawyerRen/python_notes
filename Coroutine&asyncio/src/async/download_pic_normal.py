import requests


def download_pic(url: str):
    response = requests.get(url)
    file_name = url.rsplit("_")[-1]
    with open(file_name, 'wb') as file_obj:
        file_obj.write(response.content)


if __name__ == '__main__':
    url_list = []
    for url in url_list:
        download_pic(url)
