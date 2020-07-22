import pandas as pd


if __name__ == "__main__":

    data_path = './Files/Tables.csv'
    column_names = ["Table_Name","Column_Name","Data_Type {nullable, unique}","Anonymization_Type {None, Omit, Randomize, Default value, Encode}"]
    reader = pd.read_csv(data_path, names=column_names, skiprows=1, na_values="?", sep=",", skipinitialspace=True)

    for i in range(0,(len(reader) - 1) ):
        table_path = './Files/' + reader['Table_Name'][i] + '.csv'
        table_column_names = reader['Table_Columns_Name']
        table_reader = pd.read_csv(table_path, names=table_column_names, skiprows=1, na_values="?", sep=",", skipinitialspace=True)

        # this is the data that needs to be protected
        protectedList = table_reader[reader["Column_Name"][i]]


        # call functions for anonymization














