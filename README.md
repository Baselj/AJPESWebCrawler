# Read Ajpes website - Python web crawler

## Features

Read AJPES website, click through the public auctions, download and merge PDF public auction files and send it in an e-mail.

## Requirements

1. Script uses Selenium driver to control Chrome web browser, correct version of selenium driver for your Chrome web browser is required. 
2. Create a SeleniumDrivers folder and download latest driver from [ChromeDriver](https://chromedriver.chromium.org/downloads)
3. Required Python packages are documented in requirements.txt, see [instructions how to install packages](https://learn.microsoft.com/en-us/visualstudio/python/managing-required-packages-with-requirements-txt?view=vs-2022)
4. 

## How do I use it?

- Configure your gmail account to enable automation of emails 
- Configure variables
  - mailUname (your gmail address), 
  - mailPwd (your gmail password) 
  - fromEmail (send from email address)
  - recipientEmail (recipient email list, divided by ;)

## Exmaple

Example of merged pdf can be found in [DownloadFolder/send](https://github.com/Baselj/PythonAJPESWebCrawler/blob/main/DownloadFolder/send/2022-09-26AjpesDrazbe.pdf)
