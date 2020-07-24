import pandas as pd
import random as rd


def none_function(table_data, column_data, column_name):
    return pd.DataFrame(table_data)


def omit(table_data, column_data, column_name):
    table_data.drop(columns=[column_name], axis=1, inplace=True)
    return table_data


def null_function(table_data, column_data, column_name):
    table_data.drop(columns=[column_name], axis=1, inplace=True)
    table_data[column_name] = [0] * len(column_data)
    return table_data


def default(table_data, column, column_name):
    dictionary = {value: i for i, value in enumerate(column.unique())}
    table_data[column_name].replace(dictionary, inplace=True)
    return table_data


def random(table_data, column, column_name):
    list_of_random_unique = rd.sample(range(1, len(column) * 10), len(column))
    table_data.drop(column_name, axis=1, inplace=True)
    table_data[column_name] = list_of_random_unique
    return table_data


def random_pseudonym(table_data, column, column_name):
    dictionary = {}
    for value in column:
        sample = rd.sample(range(1, len(column) * 10), len(column))
        if value not in dictionary.values():
            dictionary[value] = sample
    table_data[column_name].replace(dictionary, inplace=True)
    return table_data


def random_from_set(table_data, column_data, column_name):
    return pd.DataFrame(table_data)


def switch_function(function_name, column_data, column_name, table_data):
    if 'None-function' == function_name:
        return none_function(table_data, column_data, column_name)

    if 'Omit' == function_name:
        return omit(table_data, column_data, column_name)

    if 'Null-function' == function_name:
        return null_function(table_data, column_data, column_name)

    if 'Default' == function_name:
        return default(table_data, column_data, column_name)

    if 'Random' == function_name:
        return random(table_data, column_data, column_name)

    if 'RandomFromSet' == function_name:
        return random_from_set(table_data, column_data, column_name)

    if 'RandomPseudonym' == function_name:
        return random_pseudonym(table_data, column_data, column_name)

    return 'Invalid function name'


if __name__ == "__main__":
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
        protected_column_name = reader["Column_Name"][i]
        protectedList = table_reader[protected_column_name]

        # see which function should be used for anonymization
        anonymization_type = reader['Anonymization_Type {None, Omit, Randomize, Default value, Encode}'][i]

        # call functions for anonymization
        anonymized = switch_function(anonymization_type, protectedList, protected_column_name, table_reader)

        # new table path
        new_table_path = table_path[:-4] + '-anonymized.csv'

        # create new file
        f = open(new_table_path, "w+")
        f.close()

        # write to file
        anonymized.to_csv(new_table_path, index=False)
