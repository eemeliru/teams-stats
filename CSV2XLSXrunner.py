import glob
import win32com.client
import os

def main():
    #Converts all Teams-made-pseudo-CSVs to .XLSX
    #Opens Excel & choose the attendanceReports -folder when Excel macro pops up the window
    print("The pop up window may be in the background!")
    if os.path.exists('CSVtoXLSX.xlsm'):
        xl = win32com.client.Dispatch('Excel.Application')
        xl.Workbooks.Open(os.getcwd()+'/CSVtoXLSX.xlsm')
        xl.Application.Run("CSVtoXLS")
        xl.Application.Quit()

    #Ja poistetaan vanhat .csv:t
    for file_name in glob.glob('./attendanceReports/*.csv'):
        os.remove(file_name)

if __name__ == "__main__":
    main()