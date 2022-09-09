from bs4 import BeautifulSoup
import requests

# This function scrapes crucial financial information from Yahoo! Finance and stores it in a dicitonary
# The function serves no real purpose in Algobot yet, so I figured I'd remove the function until I decide to
# implement it


def scrape_indicators(ticker):

    # Obtain HTML for search page
    base_url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker
    edgar_resp = requests.get(base_url)
    edgar_str = edgar_resp.text

    soup = BeautifulSoup(edgar_str, 'html.parser')
    # Finds the two table objects that contain the indicators we want
    indicators = {}
    table_tag = soup.find(
        'table',
        {'class': ['W(100%)', 'W(100%) M(0) Bdcl(c)']})
    rows = table_tag.find_all('tr')
    for row in rows:
        # Finds labels for the data
        labels = row.find_all('span')
        # Finds the values for the data
        values = row.find_all(
            'td',
            attrs={'class': 'Ta(end) Fw(600) Lh(14px)'})
        # Adds each value to the dict indicators
        # labels and values are lists, so we need to get the first item in the list
        # then get the text for that
        indicators[labels[0].get_text()] = values[0].get_text()
    return indicators


def scrape_weights():

    # Obtain HTML for search page
    base_url = "https://www.slickcharts.com/sp500"
    edgar_resp = requests.get(base_url)
    edgar_str = edgar_resp.text

    # Find the document link
    soup = BeautifulSoup(edgar_str, 'html-parser')
    # Finds the two table objects that contain the indicators we want
    weights = {}
    table_tag = soup.find_all('table',
                              {'class': ['table table-hover table-borderless table-sm']})
    rows = table_tag.find_all('tr')
    for row in rows:
        # Finds labels for the data
        labels = row.find_all('span')
        # Finds the values for the data
        values = row.find_all('td')
        # Adds each value to the dict indicators
        # labels and values are lists, so we need to get the first item in the list
        # then get the text for that
        weights[labels[0].get_text()] = values[0].get_text()

    return weights


# print(scrape_indicators('AMZN'))

print(scrape_weights())
