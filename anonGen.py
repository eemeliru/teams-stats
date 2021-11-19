import pandas as pd

from mimesis import Person
person = Person('fi')

def main():
    df = pd.read_csv('AllDataPreprocessed.csv')
    df['Duration'] = pd.to_numeric(df['Duration'], downcast='float')

    arr = df['Full Name'].unique()

    for name in arr:
        anon = person.full_name()

        df.loc[df['Full Name'] == name, ['Full Name']] = anon

    df.to_csv('anonData.csv', index=False)

if __name__ == '__main__':
    main()