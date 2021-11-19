import pandas as pd
import glob
import openpyxl
import re
import os

def main():
    #Load all .xlsx -files from attendanceReports -folder
    df_raw = pd.DataFrame()
    skippedRows = 0
    for file_Name in glob.glob('./attendanceReports/*.xlsx'):
        wb = openpyxl.load_workbook(file_Name)
        sheet = wb.active
        #Teams generates sometimes Meeting id to the report (or more specifically, didn't generate Meeting ID at first..)
        if(sheet['A6'].value == 'Meeting Id'):
            skippedRows = 7
        else:
            skippedRows = 6
        
        #Reads file from row skippedRows+1 onwards
        x = pd.read_excel(file_Name, skiprows=skippedRows)
        df_raw = pd.concat([df_raw,x],axis=0)


    # Function to clean the organisation tags from Names
    def clean_Names(Name):
        # Search for opening bracket in the Name followed by
        # any characters repeated any number of times
        if re.search('\(.*', Name):

            # Extract the position of beginning of pattern
            pos = re.search('\(.*', Name).start()

            # return the cleaned Name
            return Name[:pos]

        else:
            # if clean up needed return the same Name
            return Name

    #Make copy of dataframe (relic from debugging times)
    df = df_raw.copy()
    #Drop NaNs and columns that have no useful information
    df = df.drop(df.columns[4:], axis = 1)
    df = df.dropna()
    df = df.reset_index(drop=True)

    #Here you can edit some data if you wish
    #E.g. Matti has joined once from phone and now has one entry as Matti, not Meikäläinen Matti:
    #df['Full Name'] = df['Full Name'].replace({'Matti': 'Meikäläinen Matti (Organisaatio)'})
    #Removes organisation tägs from Names
    df['Full Name'] = df['Full Name'].apply(clean_Names)

    #Duration -column to minutes
    #Teams generates the time spent in meeting -column different ways, so we loop through all known cases
    for i in df.index:
        try:
            df.loc[i, 'Duration']
            df.loc[i, 'Duration'] = pd.to_datetime(df.loc[i, 'Duration'], format='%Hh %Mm')
            df.loc[i, 'Duration'] = df.loc[i, 'Duration'].hour * 60 + df.loc[i, 'Duration'].minute
        except ValueError:
            try:
                df.loc[i, 'Duration'] = pd.to_datetime(df.loc[i, 'Duration'], format='%Hh ')
                df.loc[i, 'Duration'] = df.loc[i, 'Duration'].hour * 60
            except ValueError:
                try:
                    df.loc[i, 'Duration'] = pd.to_datetime(df.loc[i, 'Duration'], format='%Mm %Ss') 
                    df.loc[i, 'Duration'] = df.loc[i, 'Duration'].minute + df.loc[i, 'Duration'].second / 60
                except ValueError:
                    try:
                        df.loc[i, 'Duration'] = pd.to_datetime(df.loc[i, 'Duration'], format='%Mm ') 
                        df.loc[i, 'Duration'] = df.loc[i, 'Duration'].minute + df.loc[i, 'Duration'].second / 60
                    except ValueError:
                        df.loc[i, 'Duration'] = pd.to_datetime(df.loc[i, 'Duration'], format='%Ss')
                        df.loc[i, 'Duration'] = df.loc[i, 'Duration'].second / 60
        except:
            print("Error???")

    #Delete duplicates and reindex whole dataframe before saving as .csv -file
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    df.to_csv('AllDataPreprocessed.csv', index=False)

if __name__ == "__main__":
    main()