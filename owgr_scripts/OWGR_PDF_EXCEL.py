import tabula as tb
import pandas as pd
import datetime


weeks = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20',
         '21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40',
         '41','42','43','44','45','46','47','48','49','50','51','52']

YEAR= "2021"

for run, week in enumerate(weeks):
    # Enter path where PDF's are stored. The Excel file will be saved in the same folder
    path = f'C:/Users/adamr/OneDrive/Documents/Work/Portfolio Projects/PGA-stats/{YEAR}/'
    fname = f'{YEAR}_{week}OWGR.pdf'

    # Check to see if a valid PDF exists for the week provided
    try:
        df = tb.read_pdf(path + fname, pages='all')

        list1 = []
        for item in df:
            for info in item.values:
                list1.append(info)

        df = pd.DataFrame(list1)
        df1 = df.drop(range(0, 2))
        df2 = df1[(df1[0].str.contains('This') == False) & (df1[0].str.contains('Week') == False)]
        df2.reset_index(drop=True, inplace=True)

        col_names = ['This Week', 'Last Week', 'End Prev Year', 'Name', 'Country', 'Ave Points', 'Total Points',
                     'Events Played','Points Lost in Year', 'Points Gained in Year', 'Events Played (Act)']
        df2.columns = col_names
        df2['Last Week'] = df2['Last Week'].str.replace('-', '')
        # df2['Last Week'] = df2['Last Week'].str.replace(')', '')
        df2['End Prev Year'] = df2['End Prev Year'].str.replace('<', '')
        df2['End Prev Year'] = df2['End Prev Year'].str.replace('>', '')
        #df2.to_csv('outfile3.csv')

        df3 = df2[['This Week', 'End Prev Year', 'Name', 'Country', 'Events Played (Act)']]

        # Insert Column for the Week Of
        rankDate = f'{YEAR} {week}'
        weekOf = (datetime.datetime.strptime(rankDate + ' 0', "%Y %W %w") - datetime.timedelta(days=7)).date()
        df3['WEEK OF'] = weekOf
        df3.to_csv(path+f'OWGR_{weekOf}.csv')

    # Skip excel conversion of PDF if valid PDF does not exist (Sometimes a V2 is published on OWGR website and the PDF
    # that gets downloaded from the main URL is corrupt.
    except:
        continue


