#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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


def save_csv(arranged, filename):
    """
    function that saves the dataframe to csv.
    :param arranged: a pandas dataframe, to be plotted.
    """
    try:
        arranged.to_csv(path_or_buf=filename)
    except Exception as e:
        print("error occurred while saving csv...", e)


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


def main():
    df = load_csv('crimes.csv')
    processed_df = process_df(df)
    save_csv(processed_df, 'result.csv')
    plot(processed_df)


if __name__ == "__main__":
    main()
