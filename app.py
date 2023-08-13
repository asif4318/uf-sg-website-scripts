from bs4 import BeautifulSoup
import requests
import os

url = 'https://sg.ufl.edu/branches/legislative/senate-resources/'
download_folder = 'bills'

# Create the download folder if it doesn't exist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

pdf_links_with_keywords = []

for link in soup.find_all('a', href=True):
    href = link['href'].lower()
    if href.endswith('.pdf') and ('ssb' in href or 'bill' in href):
        pdf_links_with_keywords.append(link['href'])

for pdf_link in pdf_links_with_keywords:
    # Extract the filename from the URL
    filename = pdf_link.split('/')[-1]

    # Construct the full path to save the file
    file_path = os.path.join(download_folder, filename)

    # Download the PDF file
    pdf_response = requests.get(pdf_link)
    with open(file_path, 'wb') as pdf_file:
        pdf_file.write(pdf_response.content)
        print(f"Downloaded: {filename}")
