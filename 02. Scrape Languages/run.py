import requests, os
from bs4 import BeautifulSoup

# Script to download all the language data from UniMorph
#
# I made use of the link format - [ 'https://raw.githubusercontent.com/unimorph/',iso,'/master/',iso ]
#
# Steps:
#
#     - get_langs_and_wals()
#         - Scrape the languages from the HTML table in [ 'https://unimorph.github.io/' ]
#         - Store them [ Language, ISO ] in [ scraped.txt ]
#
#     - download_all_langs_files()
#         - Reads the [ scraped.txt ]
#         - Reads and download the files making use of link format
#
#     - RESULTS: All the languages data downloaded

def get_langs_and_wals():
    """ Scrapes all the data [Language, ISO] from unimorph website """

    url = 'https://unimorph.github.io/'
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    # Empty the file if it exists
    open('scraped.txt', 'w').close()

    for tr in soup.findAll("table"):
        for td in tr.find_all("td"):
            if td.attrs.get('style') == "font-family: monospace":
                # Write to the [ ISO, Language ] to the file
                with open('scraped.txt','a',encoding='utf-8') as outFile:
                    iso = td.text
                    language = str(prev)[6: str(prev).find("</t") ]
                    line = " ".join( [iso, language ] )
                    outFile.write(line + '\n')

            # To save the language [ one place before the ISO ]
            elif not td.attrs.get('style'):
                prev = (td.encode('utf-8'))


def download_all_langs_files():
    """ Reads the languages and ISO from scraped.txt and downloads the files """
    it = 0
    # Create the folder containing all languages data
    try:
        here = os.path.dirname(os.path.realpath(__file__))
        dir_name = 'Languages'
        os.mkdir(os.path.join(here, dir_name))
    except FileExistsError:
        print("\nERROR\nLanguage folder already exists!\nPlease remove/rename it to continue!")


    with open('scraped.txt','r') as all_file:
        for line in all_file:
            it += 1
            if it==50:
                break
            # Prepares format
            line_content = line.split()
            iso = line_content[0]
            language = " ".join(line_content[1:]).lower()
            file_name = ''.join([language,'.csv'])
            # Create the file path
            file_path = os.path.join(here, dir_name, file_name)
            # Creates the url
            url = ''.join(['https://raw.githubusercontent.com/unimorph/',iso,'/master/',iso])
            r = requests.get(url, allow_redirects=True)
            # Write to file
            open(file_path, 'wb').write(r.content)
        print("\nDone")

get_langs_and_wals()
download_all_langs_files()
