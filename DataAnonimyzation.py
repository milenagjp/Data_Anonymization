import pandas as pd


if __name__ == "__main__":

    data_path = './Files/Tables.csv'
    column_names = ["Table_Name","Column_Name","Data_Type {nullable, unique}","Anonymization_Type {None, Omit, Randomize, Default value, Encode}", 'Table_Column_Name']
    reader = pd.read_csv(data_path, encoding="windows-1252", names=column_names, skiprows=1, na_values="?", sep=",", skipinitialspace=True)

    # go though all tables and do stuff
    for i in range(0,(len(reader) - 1)):
        table_path = './Files/' + reader['Table_Name'][i] + '.csv'
        string_list = reader['Table_Column_Name'][i]
        table_column_names = string_list[0:-1].split(',')

        # reading table data
        table_reader = pd.read_csv(table_path, encoding="windows-1252", names=table_column_names, skiprows=1, na_values="?", sep=",", skipinitialspace=True)

        # this is the data from the column that needs to be protected
        protectedList = table_reader[reader["Column_Name"][i]]


        # call functions for anonymization


