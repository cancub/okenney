# This program gets the holdings of a specified ETF from www.barchart.com
# and computes the actual equity you have for each company.
# At the end of the operation, the program saves this information into .csv file
# and shows you bar plot.

from bs4 import BeautifulSoup
import argparse
import matplotlib
import matplotlib.pyplot as plt
import re
import requests
import numpy as np
import pandas as pd
import time
'''
brew install phantomjs
or
brew tap homebrew/cask
brew cask install chromedriver
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import os
# from selenium.webdriver.chrome.webdriver import WebDriver

def get_etf_holdings(etf_symbol):
    '''
    etf_symbol: str
    
    return: pd.DataFrame
    '''
    url = 'https://www.etf.com/{}#overview'.format(etf_symbol)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')

    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
    # current directory
    chrome_driver='/usr/bin/chromedriver'


    # Loads the ETF constituents page and reads the holdings table
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    browser.get(url)
    while True:
        try:
            browser.find_element_by_css_selector('#top10HoldingsAppContainer .link-blue').click()
            break
        except ElementClickInterceptedException:
            time.sleep(0.1)
    while True:
        try:
            table = browser.find_element_by_class_name('view_all_table')
            break
        except NoSuchElementException:
            time.sleep(0.1)

    html = table.get_attribute('innerHTML')
    table = BeautifulSoup(html, 'html.parser')

    # Reads the holdings table line by line and appends each asset to a
    # dictionary along with the holdings percentage
    asset_dict = {}
    for row in table.select('tr'):
        cells = row.select('td')
        description = cells[0]
        try:
            company_info = description.select('a')[0]
        except Exception:
            continue
        
        name = company_info.text
        ticker = company_info['href'].split('/')[-1]
        percent = cells[1].text.rstrip('%')
        asset_dict[ticker] = {'name': name, 'percent': percent}
    browser.quit()
    return pd.DataFrame.from_dict(asset_dict, orient='index')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('etf', help='Name of ETF')
    args = parser.parse_args()

    df = get_etf_holdings(args.etf)
    df.sort_values(by='percent', axis=0, ascending=False,
                    inplace=True, na_position='last')
    csv_name = args.etf+'.csv'
    df.to_csv(csv_name, sep=';')

    # Plotting
    # ax = df.plot.bar(y='equity')
    # # plt.xticks(rotation=45)
    # plt.xlabel('Companies')
    # plt.ylabel('Equity')
    # plt.grid()
    # plt.show()

if __name__ == '__main__':
    main()