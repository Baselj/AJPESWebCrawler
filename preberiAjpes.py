#pip install selenium
#pip install PyPDF2

from asyncio.windows_events import NULL
import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import glob
import stat
import os
import shutil
from PyPDF2 import PdfFileMerger
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import sys

osnovniFolder =os.path.dirname(os.path.realpath(__file__))
downloadFolder = osnovniFolder+r"\DownloadFolder"
chromeDriverFolder = osnovniFolder+ r"\SeleniumDrivers\chromedriver.exe"
#konfiguracija gmail

mailUname=""
mailPwd=""
fromEmail=""

kolikoVrsticZelim = "500"
mailBody=""
randomZakasnitev = random.randint(1,3)
url='https://www.ajpes.si/eObjave/rezultati.asp?podrobno=0&id_skupina=51&TipDolznika=-1&TipPostopka=-1&id_SkupinaVrsta=-1&id_skupinaPodVrsta=-1&Dolznik=&Oblika=&MS=&DS=&StStevilka=&Sodisce=-1&DatumDejanja_od=&DatumDejanja_do=&sys_ZacetekObjave_od=&sys_ZacetekObjave_do=&MAXREC='+kolikoVrsticZelim
tekstZaDll =["razpis dražbe / vabila k dajanju ponudb"]


def posljiEmail(mailBody,priponka,prejemniki):
    smtpHost="smtp.gmail.com"
    smtpPort=587

    if mailBody == "":
        mailSubject ="Ni novih AJPES drazb dne " + str(datetime.date.today())
    else:
        mailSubject= "AJPES drazbe dne " + str(datetime.date.today())

    mailContentHTML= mailBody
    if mailContentHTML =="":
        mailContentHTML="Ni novih "+r"<a href='"+url+r"'>AJPES drazb</a>" +" dne " + str(datetime.date.today())
    msg=MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = ','.join(prejemniki)
    msg['Subject']=mailSubject
    msg.attach(MIMEText(mailContentHTML, 'html'))

    #priponka
    if  mailBody !="":
        part=MIMEBase('application', 'octet-stream')
        part.set_payload(open(priponka,"rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="{0}"'.format(priponka.split(os.sep)[-1]))
        msg.attach(part)

    s=smtplib.SMTP(smtpHost,smtpPort)
    s.starttls()
    s.login(mailUname,mailPwd)
    msgText=msg.as_string()
    sendErrs= s.sendmail(fromEmail, prejemniki, msgText)
    s.quit()

    if not len(sendErrs.keys()) ==0:
        raise Exception("Errors occured while sending email", sendErrs)

    
def dobiZadnjiFile(folder):
    file_type = r'\*pdf'
    files = glob.glob(folder + file_type)
    if len(files) != 0:
        return max(files, key=os.path.getctime),max(files, key=os.path.getctime).split(os.sep)[-1]
    else:
        return folder,glob.glob(folder+"/*")[0].split(os.sep)[-1]

def ustvariFolderSkopiraj(fileSrc,fileDest):
    if not os.path.exists(fileDest):
        os.makedirs(fileDest)
    os.chmod(fileDest, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    shutil.copy(fileSrc,fileDest)
        
def brisiFolderUstvariNovega(folder):
        folder= folder
        os.chmod(folder, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        shutil.rmtree(folder, ignore_errors=False)
        if not os.path.exists(folder):
            os.makedirs(folder)
            os.chmod(folder, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

def brisiFolderCePrevelik(folder,maxvelikost):
    size = 0

    for path, dirs, files in os.walk(folder):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)

    if size>maxvelikost:
        os.chmod(folder, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        shutil.rmtree(folder, ignore_errors=False)
        os.makedirs(folder)
        os.chmod(folder, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

def zdruziVsePdf (folder):
        folder= folder
        pdfs = os.listdir(folder)
        # os.listdir will create the list of all files in a directory
        merger = PdfFileMerger(strict=False)
        for file in pdfs:
            if file.endswith(".pdf"):
                path_with_file = os.path.join(folder, file)
                merger.append(path_with_file,  import_bookmarks=False )
        pot=folder+'\\'+datetime.datetime.today().strftime('%Y-%m-%d')+"AjpesDrazbe.pdf"
        merger.write(pot)
        merger.close()
        return pot

s=Service(chromeDriverFolder)

chrome_options = webdriver.ChromeOptions()
chrome_options = Options()
#chrome_options.add_argument("--headless")

chrome_options.add_experimental_option("prefs", {
        "download.default_directory": downloadFolder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})

browser = webdriver.Chrome(service=s, options= chrome_options)

browser.get(url)
tableRezultati= browser.find_element(By.ID, "tableRezultati")

prvic=True
time.sleep(randomZakasnitev)
if tableRezultati.find_elements(By.XPATH, ("//*[contains(text(),'DOVOLIM')]")) and prvic:
    tableRezultati.find_element(By.XPATH, ("//*[contains(text(),'DOVOLIM')]")).click()
vrstice = tableRezultati.find_elements(By.TAG_NAME, "tr")    
mailZacetek = r"<a href='"+url+r"'>AJPES drazbe</a><br>" 
mailBody=mailZacetek
for vrstica in vrstice:
    if vrstica.find_elements(By.TAG_NAME, "a"):
        #je to edini odprti tab?
        #assert len(browser.window_handles)==1
        pov= vrstica.find_element(By.TAG_NAME, "a")
        if pov.text == tekstZaDll[0]:
            time.sleep(randomZakasnitev)
            pov.send_keys(Keys.CONTROL+Keys.ENTER)
            browser.switch_to.window(browser.window_handles[1])
            if browser.find_elements(By.XPATH, ("//*[contains(text(),'DOVOLIM')]")) and prvic:
                browser.find_element(By.XPATH, ("//*[contains(text(),'DOVOLIM')]")).click()
                time.sleep(randomZakasnitev)
                prvic=False
            datum=datetime.datetime.strptime(browser.find_element(By.XPATH, ("//*[contains(text(),'Datum objave:')]/following-sibling::th")).text,'%d.%m.%Y   %H:%M')
            datumString=datum.strftime("%Y-%m-%d %H:%M")
            
            browser.find_element(By.XPATH, ("//*[contains(text(),'Vsebina procesnega dejanja')]")).click()
            time.sleep(randomZakasnitev)
            tekstBody= (datumString + " - "+browser.find_element(By.XPATH, ("//*[contains(text(),'Sodišče')]/following-sibling::th")).text + " - "+browser.find_element(By.XPATH, ("//*[contains(text(),'Dolžnik')]/following-sibling::th")).text)+ os.linesep +"<br>"
            WebDriverWait(browser, 120, 1).until(every_downloads_chrome)
            
            if ((dobiZadnjiFile(downloadFolder)[1][-7:] in ("(1).pdf","(2).pdf","(3).pdf","(4).pdf")) == False):
                
                mailBody =mailBody+ tekstBody
                
                ustvariFolderSkopiraj(dobiZadnjiFile(downloadFolder)[0],downloadFolder+"\send")
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            #v kolikor ne bi se okno dovolj hitro odprlo
             # wait.until(EC.number_of_windows_to_be(2))

potZdruzenegaPdf= (zdruziVsePdf(downloadFolder+"\send"))
browser.quit()
print(mailBody)
if mailBody==mailZacetek:
    mailBody=""
posljiEmail(mailBody,potZdruzenegaPdf,["kristof.baselj@gmail.com"])
brisiFolderUstvariNovega(downloadFolder+"\send")
brisiFolderCePrevelik(downloadFolder,2900000000)
sys.exit()
quit()