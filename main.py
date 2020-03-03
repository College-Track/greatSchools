import pandas as pd
import numpy as np
import os


def create_files_to_read(states_to_include, directory):

    files_to_read = []
    entries = os.listdir(directory)

    for entry in entries:
        if entry.split("-")[5].split(".")[0] in states_to_include:
            files_to_read.append(entry)

    return files_to_read


def read_and_concat_dfs(files_to_read, directory):
    _df_list = []

    for i in range(len(files_to_read)):
        _df = pd.read_csv(directory + files_to_read[i], sep="\t", header=0)
        _df["state"] = files_to_read[i].split("-")[5].split(".")[0]
        _df_list.append(_df)

    df = pd.concat(_df_list, axis=0, ignore_index=True)
    return df


def create_column_names(data_type, breakdown):
    if pd.isnull(breakdown) == True:
        return data_type
    else:
        return data_type + "-" + breakdown


def main():
    STATES_TO_INCLUDE = ["CA", "LA", "VA", "CO", "DC", "MD"]

    DIRECTORY = "local-gs-census-feed-flat/"

    files_to_read = create_files_to_read(STATES_TO_INCLUDE, DIRECTORY)
    df = read_and_concat_dfs(files_to_read, DIRECTORY)

    df["column_names"] = df.apply(
        lambda x: create_column_names(x["data-type"], x["breakdown"]), axis=1
    )
    print(len(df))

    df_wide = df.pivot_table(
        index=["universal-id", "entity", "state"],
        columns="column_names",
        values="value",
        aggfunc=np.sum,
    )
    df_wide.to_csv("Great_Schools_Results.csv")


if __name__ == "__main__":
    main()
