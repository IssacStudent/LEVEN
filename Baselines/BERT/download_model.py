import os

import requests
from bs4 import BeautifulSoup


def download_files(model_name, proxy=None):
    # Base URL for accessing the file list
    base_url = f"https://huggingface.co/{model_name}/tree/main"
    # Base URL for downloading files
    download_base_url = f"https://huggingface.co/{model_name}/resolve/main"
    proxies = {"http": proxy, "https": proxy} if proxy else None

    response = requests.get(base_url, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all("div", class_="col-span-8 flex items-center md:col-span-4 lg:col-span-3")
    links = [div.find("a", class_="group flex items-center truncate")["href"] for div in divs if div.find("a", class_="group flex items-center truncate")]

    if not os.path.exists("hfl/chinese-roberta-wwm-ext"):
        os.makedirs("hfl/chinese-roberta-wwm-ext")

    for link in links:
        print(link)
        # Extract the relative path from the 'href' attribute
        relative_path = link.replace(f"/{model_name}/blob/main/", "")
        # Construct the full URL for file downloading
        file_url = f"{download_base_url}/{relative_path}?download=true"
        file_name = link.split('/')[-1]
        file_path = os.path.join("hfl/chinese-roberta-wwm-ext", file_name)
        with requests.get(file_url, stream=True, proxies=proxies) as r:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    print("finished!")

# Example usage
download_files("hfl/chinese-roberta-wwm-ext", "http://127.0.0.1:7890")  # With proxy
