import pandas as pd
import random as rd


def default(df, column, column_name):
    dictionary = {value: i for i, value in enumerate(column.unique())}
    df[column_name].replace(dictionary, inplace=True)
    print(df)
    return df


def random(df, column, column_name):
    list_of_random_unique = rd.sample(range(1, len(column) * 10), len(column))
    df.drop(column_name, axis=1, inplace=True)
    df[column_name] = list_of_random_unique
    return df


def randomPseudonym(df, column, column_name):
    dictionary = {}
    for value in column:
        sample = rd.sample(range(1, len(column) * 10), len(column))
        if value not in dictionary.values():
            dictionary[value] = sample
    df[column_name].replace(dictionary, inplace=True)
    return df


if __name__ == "__main__":
    i = 0
    data_path = './Files/Tables.csv'
    column_names = ["Table_Name", "Column_Name", "Data_Type {nullable, unique}",
                    "Anonymization_Type {None, Omit, Randomize, Default value, Encode}", 'Table_Column_Name']
    reader = pd.read_csv(data_path, encoding="windows-1252", names=column_names, skiprows=1, na_values="?", sep=",",
                         skipinitialspace=True)

    # go though all tables and do stuff
    for i in range(0, (len(reader) - 1)):
        table_path = './Files/' + reader['Table_Name'][i] + '.csv'
        string_list = reader['Table_Column_Name'][i]
        table_column_names = string_list[0:-1].split(',')

        # reading table data

        table_reader = pd.read_csv(table_path, encoding="windows-1252", names=table_column_names, skiprows=1,
                                   na_values="?", sep=",", skipinitialspace=True)
        # this is the data from the column that needs to be protected
        protectedList = table_reader[reader["Column_Name"][i]]
        # print(reader['Table_Name'][i])
        # print(protectedList)
        # call functions for anonymization
        if reader['Table_Name'][i] == 'Purchasing.Vendor':
            anonymized = default(table_reader, protectedList, reader["Column_Name"][i])
            anonymized.to_csv(table_path, index=False)

        if reader['Table_Name'][i] == 'Sales.CreditCard' or reader['Table_Name'][i] == 'Purchasing.PurchaseOrderHeader':
            anonymized = random(table_reader, protectedList, reader["Column_Name"][i])
            anonymized.to_csv(table_path, index=False)

        if reader['Table_Name'][i] == 'Production.Product' or reader['Table_Name'][i] == 'HumanResources.Employee':
            anonymized = randomPseudonym(table_reader, protectedList, reader["Column_Name"][i])
            anonymized.to_csv(table_path, index=False)
