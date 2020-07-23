import pandas as pd


def read_data():
    data_path = './Files/Tables.csv'
    column_names = ["Table_Name", "Column_Name", "Data_Type {nullable, unique}",
                    "Anonymization_Type {None, Omit, Randomize, Default value, Encode}"]
    reader = pd.read_csv(data_path, encoding="windows-1252", names=column_names, skiprows=1, na_values="?", sep=",",
                         skipinitialspace=True)

    for i in range(0, (len(reader) - 1)):
        table_path = './Files/' + reader['Table_Name'][i] + '.csv'
        table_column_names = reader['Column_Name']
        table_reader = pd.read_csv(table_path, encoding="windows-1252", names=table_column_names, skiprows=1,
                                   na_values="?", sep=",", skipinitialspace=True)

        # this is the data that needs to be protected
        protectedList = table_reader[reader["Column_Name"][i]]
        return protectedList


if __name__ == "__main__":
    protectedList = read_data()

    # call functions for anonymization
