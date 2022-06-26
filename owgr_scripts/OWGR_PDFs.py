import requests
import tabula as tb
import pandas as pd


path = '---ENTER PATH TO SAVE PDFs TO------------'


weeks = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15',
         '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30',
         '31','32','33','34','35','36','37','38','39','40','41','42','43','44','45',
         '46','47','48','49','50','51','52']

years = ['2021']


for year in years:
    for week in weeks:

        owgr_pdf_url = "http://www.owgr.com/archive/PastRankings/{}/Rankings/owgr{}f{}.pdf".format(year,week,year)

        #URL below used for earlier than 2021. "Rankings" removed from URL
        # owgr_pdf_url = "http://www.owgr.com/archive/PastRankings/{}/owgr{}f{}.pdf".format(year, week, year)
        r = requests.get(owgr_pdf_url, stream=True)

        with open(f"{path}/{year}_{week}OWGR.pdf", "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)









