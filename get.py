from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

url = 'https://vga256.com/ultima/home.html'

request_page = urlopen(url)
html = request_page.read()
request_page.close()

f = open('public/home.html', 'w')
f.write(html.decode())
f.close()

html_soup = BeautifulSoup(html, 'html.parser')

urls_to_process = []
urls_not_processed = []
urls_processed = []

for link in html_soup('a'):
    if 'http' not in link['href']:
        urls_to_process.append(f"https://vga256.com/ultima/{link['href']}")

for url in urls_to_process:
    if url not in urls_processed:
        print(f"Fetching {url}...")
        try:
            request_page = urlopen(url)
        except:
            urls_not_processed.append(url)
            continue
        
        data = request_page.read()
        request_page.close()

        file_path = url.split('https://vga256.com/ultima/')[-1]
        path_root = 'https://vga256.com/ultima/'

        if '/' in file_path:
            directories = file_path.split('/')
            file_name = directories[-1]
            full_directory = os.getcwd() + '/public/'
            for directory in directories:
                if directory != file_name:
                    path_root += directory + '/'
                    full_directory += directory + '/'
            
            os.makedirs(full_directory, exist_ok=True)

        if '.txt' in url or '.html' in url or '.htm' in url:
            f = open(f"public/{file_path}", 'w')
            content = data.decode('utf-8', errors='ignore').encode('utf-8')
            f.write(content.decode())
            f.close()

            html_soup = BeautifulSoup(data, 'html.parser')

            for link in html_soup('a'):
                if 'href' in link.attrs.keys():
                    if ':' not in link['href'] and ('.htm' in link['href'] or '.html' in link['href'] or '.txt' in link['href'] or '.jpg' in link['href'] or '.gif' in link['href']):
                        urls_to_process.append(f"{path_root}{link['href']}")
                    else:
                        if ':' in link['href']:
                            urls_not_processed.append(link['href'])
                        else:
                            urls_not_processed.append(f"{path_root}{link['href']}")
            for img in html_soup('img'):
                if 'src' in img.attrs.keys():
                    if ':' not in img['src'] and ('.jpg' in img['src'] or '.gif' in img['src']):
                        urls_to_process.append(f"{path_root}{img['src']}")
        else:
            f = open(f"public/{file_path}", "wb")
            f.write(data)
            f.close()

        urls_processed.append(url)

print("URLs not processed:")

for url in urls_not_processed:
    print(url)
