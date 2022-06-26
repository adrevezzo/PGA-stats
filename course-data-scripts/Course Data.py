import requests
import json
import pandas as pd

years = ['2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012']
tot_results = []
for year in years:

    # WARNING: The API may be closed to public access now.
    j_son = f'https://statdata-api-prod.pgatour.com/api/clientfile/HistoricalSchedules?T_CODE=r&Year={year}&format=json'
    page = requests.get(j_son)
    text = json.loads(page.text)

    try:
        courses = text['data']
    except:
        continue

    for i, trn in enumerate(courses):
        temp_list = []
        trn_id = courses[i]['ID']
        trn_end = courses[i]['END_DATE']
        perm_num = courses[i]['PERM_NUM']
        yr = courses[i]['YEAR']
        nm = courses[i]['NAME']
        prs = courses[i]['PURSE']
        crse = courses[i]['COURSE_NAME']
        cty = courses[i]['CITY']
        st = courses[i]['STATE']
        cnty = courses[i]['COUNTRY']
        wn = courses[i]['FIRST_NAME'] + ' ' + courses[i]['LAST_NAME']

        temp_list = [trn_id, trn_end, perm_num, yr, nm, prs, crse, cty, st, cnty, wn]
        tot_results.append(temp_list)

    course = pd.DataFrame(tot_results,
                          columns=['Tournament ID', 'Tournament End Date', 'Perm Num', 'Year', 'Tournament Name', 'Purse',
                                   'Course Name', 'City', 'State',
                                   'Country', 'Winner'])

    course.set_index('Course Name', inplace=True)

    # print(res.head())

course.to_csv(fr"----ETNER YOUR FOLDER PATH HERE----\Courses.csv")

