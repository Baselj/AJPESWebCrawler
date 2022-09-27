# Read Ajpes website - Python web crawler

## Features

Read AJPES website, click through the public auctions, download and merge PDF public auction files and send it in an e-mail.

## Requirements

1. Python 3.10
2. Selenium driver for Chrome web browser
3. PyPDF2

Script uses selenium driver to control Chrome web browser, correct version of selenium driver for your Chrome web browser is required. Required Python packages are documented in requirements.txt, see [instructions how to install packages](https://learn.microsoft.com/en-us/visualstudio/python/managing-required-packages-with-requirements-txt?view=vs-2022)

## How do I use it?

- Configure your gmail account to enable automation of emails 
- Configure variables
  - mailUname (your gmail address), 
  - mailPwd (your gmail password) 
  - fromEmail (send from email address)
  - recipientEmail (recipient email list, divided by ;)

## Exmaple

Example of merged pdf can be found in [DownloadFolder/sned](https://github.com/Baselj/PythonAJPESWebCrawler/blob/main/DownloadFolder/send/2022-09-26AjpesDrazbe.pdf)
