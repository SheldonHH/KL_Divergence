import pandas as pd
import sidetable
raw_data_path = 'data_sample/trimmed_user_1_data.csv'


def read_from_csv():
    df = pd.read_csv(raw_data_path)
    print(df['x'].value_counts())


def main():
    read_from_csv()


if __name__ == "__main__":

    main()
