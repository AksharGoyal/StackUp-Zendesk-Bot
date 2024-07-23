import json
import requests
import re
# import html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

URL = 'https://stackuphelpcentre.zendesk.com/api/v2/help_center/en-us/articles?per_page=150'

def json_fetcher(url):
    """
    Fetches JSON data from the specified URL and saves it to a local file named 'response.json'.
    This function sends a GET request to the provided URL and retrieves the JSON data.
    If the request is successful (status code 200), the function extracts the 'articles' data from the response
    and saves it to a local file named 'response.json' using the `json.dump()` function.
    If an exception occurs during the request or data processing, the function will print an error message
    with the exception detailsand the HTTP status code and reason.
    """
    response = requests.get(url)
    try:
        if response.status_code == 200:
            data = response.json()
            extracted_data = {'articles': data.get('articles')}
            with open('response.json', 'w') as file:
                json.dump(extracted_data, file, indent=4)
            print('Response saved to response.json successfully.')
    except Exception as e:
        print(f'Error found: {e}')
        print(f'Error: {response.status_code} - {response.reason}')
    finally:
        return


def clean_html(raw_html):
    """
    The function takes a string of raw HTML text as input and removes all HTML tags from the text, 
    returning the cleaned text. This function uses a regular expression to identify
    and remove all HTML tags from the input text.
    The `re.compile('<.*?>')` pattern matches any HTML tag, and replaces all matches with an empty string,
    effectively removing the tags. This function is a helper function used to process the article body content before
    it is added to the PDF document, ensuring that any HTML formatting is removed and the text is in a plain format.
"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def convert_links_to_markdown(text):
    '''
    The  function takes a string of text as input and converts any HTML links within the text to Markdown format.
    This is a helper function used to process the article body content before it is added to the PDF document.    
    The function uses a regular expression to identify any HTML `<a>` tags within the input text,
    and then replaces them with the Markdown link syntax `[text](url)`,
    where the text is the link text and the url is the link target.
    If the input text is empty, the function simply returns the original text unchanged.
    '''
    # Convert HTML links to Markdown format
    if not text:
        return text
    link_pattern = re.compile(r'<a href="(.*?)">(.*?)</a>')
    return re.sub(link_pattern, r'[\2](\1)', text)

def remove_non_ascii(text):
    """
    Removes any non-ASCII characters from the input text by encoding the text as ASCII
    and ignoring any non-ASCII characters.
    """
    return text.encode('ascii', 'ignore').decode('ascii')

def process_article(article):
    """
    The  function takes an article dictionary as input and returns the cleaned and formatted article body text.

    The function performs the following steps:

    1. Retrieves the 'body' field from the article dictionary, or uses 'No Body' as a default if the field is not present.
    2. Converts any HTML links within the article body to Markdown format using the `convert_links_to_markdown` function.
    3. Removes all HTML tags from the article body using the `clean_html` function.
    4. Strips any leading or trailing whitespace from the cleaned article body.
    5. Replaces all newline characters (`\n`) and carriage return characters (`\r`) with a single space character.
    6. Removes any non-ASCII characters from the article body using the `remove_non_ascii` function.

    Finally, the function returns the cleaned and formatted article body text.
    """
    
    body = article.get('body', "")
    body_cleaned = ""
    if body:
        body = convert_links_to_markdown(body)
        body_cleaned = clean_html(body).strip()
        body_cleaned = body_cleaned.replace('\n', ' ').replace('\r', '')
        body_cleaned = remove_non_ascii(body_cleaned)  # Remove non-ASCII characters
    return body_cleaned

def main():
    """
    The `main()` function is the entry point of the data scraper script. It performs the following steps:

    1. Calls the `json_fetcher()` function to fetch JSON data from a URL.
    2. Loads the fetched JSON data from the 'response.json' file.
    3. Iterates through the 'articles' list in the JSON data.
    4. For each article, it:
    - Extracts the article title, URL, and cleaned article body text.
    - Appends Paragraph and Spacer objects to a 'flowables' list, representing the formatted article content.
    5. Creates a SimpleDocTemplate object with the filename 'data/zendesk_articles.pdf'.
    6. Builds the PDF document using the 'flowables' list.
    7. Prints a message indicating that the PDF file has been created.
    """
    # Load JSON data
    json_fetcher(URL)
    with open('response.json', 'r') as file:
        data = json.load(file)
    print('Response.json is loaded')
    
    articles = data.get('articles', [])
    filename = "data/zendesk_articles.pdf"
    flowables = []
    
    for article in articles:
        title = article.get('title', '')
        # url = article.get('html_url', 'https://stackuphelpcentre.zendesk.com/hc/en-us')
        body_cleaned = process_article(article)
        flowables.append(Paragraph(f"<h1>{title}</h1>"))
        flowables.append(Spacer(5,3))
        flowables.append(Paragraph(f"{body_cleaned}"))
        flowables.append(Spacer(5,3))
        # flowables.append(Paragraph(f'<p><a href="{url}">Source</a></p>'))
        flowables.append(Spacer(5,6))
        
    doc = SimpleDocTemplate(filename)
    doc.build(flowables)
    print(f'{filename} is created.')
    
if __name__ == '__main__':
    main()