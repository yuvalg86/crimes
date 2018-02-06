#!/usr/bin/python3
"""Usage: csv_to_heatmap.py [--input=<FILE> --output=<FILE>]

Process CSV and saves some intereseting crime data per district and plots it into a heatmap.

Options:
  -h --help     prints this screen
  --input=<FILE>    input csv to load [default: crimes.csv]
  --output=<FILE>   Output csv to save [default: result.csv]
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from docopt import docopt


CSV_INDEXED_COLS = ["District", "Primary Type"]
NEW_COUNT_COL = 'Size'


def load_csv(filename):
    """
    function that loads the csv file.
    :param filename: a csv file, with CSV_INDEXED_COLS available.
    :return: dataframe containing the two CSV_INDEXED_COLS
    """
    try:
        return pd.read_csv(filename, usecols=CSV_INDEXED_COLS)
    except Exception as e:
        print("error occurred while loading csv...", e)
        exit(1)


def save_csv(arranged, filename):
    """
    function that saves the dataframe to csv.
    :param arranged: a pandas dataframe, to be plotted.
    """
    try:
        arranged.to_csv(path_or_buf=filename)
    except Exception as e:
        print("error occurred while saving csv...", e)
        exit(1)


def process_df(df):
    """
    functin that makes some changes to loaded df, and returns a resulted df.
    :param df: a pandas dataframe, with CSV_INDEXED_COLS available.
    :return: dataframe pivoted where rows are type of crime, and columns are the Districts.
    """
    try:
        # add new coloum which represents the ammount of each crime type in
        # destrict.
        added_count = df.groupby(
            CSV_INDEXED_COLS).size().reset_index(name=NEW_COUNT_COL)
        # pivot the data to use rows as districts and coloumns as type.
        pivoted = added_count.pivot(
            index=CSV_INDEXED_COLS[1],
            columns=CSV_INDEXED_COLS[0],
            values=NEW_COUNT_COL)
        # add replace NANs to 0.
        return pivoted.fillna(value=0)
    except Exception as e:
        print("error occurred while processing data...", e)
        exit(1)


def plot(arranged):
    """
    function that plots a df (of arranged type) to heatmap.
    :param arranged: a pandas dataframe, to be plotted.
    """
    try:
        plt.pcolor(arranged, cmap='hot')
        plt.yticks(np.arange(0.5, len(arranged.index), 1), arranged.index)
        plt.xticks(np.arange(0.5, len(arranged.columns), 1), arranged.columns)
        plt.title('Make crime pay. Become a lawyer. // Will Rogers')
        plt.xlabel(CSV_INDEXED_COLS[0])
        plt.ylabel('Crime')
        plt.colorbar()
        plt.show()
    except Exception as e:
        print("error occurred while plotting...", e)
        exit(1)


def main():
    arguments = docopt(__doc__, version='heatmap 0.1')
    df = load_csv(arguments['--input'])
    processed_df = process_df(df)
    save_csv(processed_df, arguments['--output'])
    plot(processed_df)


if __name__ == "__main__":
    main()
