from Stat_Functions import *
import pandas as pd
import datetime


# This file will return Driving Accuracy, SG: T2G, Driving Distance, GIR%, SG: APP, SG: ATG, SG: OTT, SG: PUTT rankings
# through the given tournament. Provide the path to store results in "path", provide at least 1 tournament number (pgatour.com
# defined) in url_num, the weekof tournament date (ending sunday), and the Tour Schedule Year in year. Can add multiple
# tournaments by adding multiple respective entries into each list, but only once schedule year at a time.

def main():

    path = fr"---ETNER FILEPATH TO SAVE RESULTS TO----"
    url_num = ['t014']
    trny_name = ['Masters Tournament']
    weekOf = [datetime.datetime.strptime('4/10/2022', '%m/%d/%Y')]
    year = '2022'

    for wk, url in enumerate(url_num):
        temp_trny = trny_name[wk]
        temp_offset = weekOf[wk]

        PGA_DA_func.pga_da(url, temp_trny, year,temp_offset, path)
        PGA_SGT2G_func.pga_sgt2g(url, temp_trny, year,temp_offset, path)
        PGA_DD_func.pga_dd(url, temp_trny, year,temp_offset, path)
        PGA_GIR_func.pga_gir(url, temp_trny, year,temp_offset, path)
        PGA_SGAPP_func.pga_sgapp(url, temp_trny, year,temp_offset, path)
        PGA_SGATG_func.pga_sgatg(url, temp_trny, year,temp_offset, path)
        PGA_SGOTT_func.pga_sgott(url, temp_trny, year,temp_offset, path)
        PGA_SGPUTT_func.pga_sgputt(url, temp_trny, year,temp_offset, path)


if __name__ == '__main__':
    main()


