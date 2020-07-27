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


def random_from_set(table_data, column_data, column_name, referenced_column_data):
    new_values = []
    for value in column_data:
        new_values.append(rd.choice(referenced_column_data))

    table_data[column_name] = new_values
    return table_data


def random_pseudonym_from_set(table_data, column_data, column_name, referenced_column_data):
    new_values = []
    referenced_column_data = referenced_column_data.to_list()
    for value in column_data:
        num = rd.choice(referenced_column_data)
        referenced_column_data.remove(num)
        new_values.append(num)

    table_data[column_name] = new_values
    return table_data


def switch_function(function_name, column_data, column_name, table_data, referenced_column = None):
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
        return random_from_set(table_data, column_data, column_name, referenced_column)

    if 'RandomPseudonym' == function_name:
        return random_pseudonym(table_data, column_data, column_name)

    if 'RandomPseudonymFromSet' == function_name:
        return random_pseudonym_from_set(table_data, column_data, column_name, referenced_column)

    return 'Invalid function name'


def get_column_data(_column_name):
    keys_path = './Files/keys.csv'
    keys_column_names = ['Ref1_Table_Name','Ref1_Column_Name','Ref2_Table_Name','Ref2_Column_Name']
    keys_reader = pd.read_csv(keys_path, names=keys_column_names, encoding="windows-1252", skiprows=1,
                              na_values="?", sep=",", skipinitialspace=True)
    referenced_column_name = ''
    table_name = ''

    for i in range(0, len(keys_reader)):
        if keys_reader['Ref1_Column_Name'][i] == _column_name:
            referenced_column_name = keys_reader['Ref2_Column_Name'][i]
            table_name = keys_reader['Ref2_Table_Name'][i]

    referenced_column_names = []
    main_table_path = './Files/Tables.csv'
    main_table_column_names = ["Table_Name", "Column_Name", "Data_Type {nullable, unique}",
                    "Anonymization_Type {None, Omit, Randomize, Default value, Encode}", 'Table_Column_Name']
    main_table_reader = pd.read_csv(main_table_path, encoding="windows-1252", names=main_table_column_names, skiprows=1, na_values="?", sep=",",
                         skipinitialspace=True)

    for i in range(0, len(main_table_reader)):
        if main_table_reader['Table_Name'][i] == table_name:
            referenced_column_names = main_table_reader['Table_Column_Name'][i].split(',')
            break

    referenced_path = './Files/' + table_name + '.csv'
    referenced_table = pd.read_csv(referenced_path, names=referenced_column_names, encoding="windows-1252", skiprows=1,
                                   na_values="?", sep=",", skipinitialspace=True)

    column_data = referenced_table[referenced_column_name]
    return column_data


if __name__ == "__main__":
    data_path = './Files/Tables.csv'
    column_names = ["Table_Name", "Column_Name", "Data_Type {nullable, unique}",
                    "Anonymization_Type {None, Omit, Randomize, Default value, Encode}", 'Table_Column_Name']
    reader = pd.read_csv(data_path, encoding="windows-1252", names=column_names, skiprows=1, na_values="?", sep=",",
                         skipinitialspace=True)

    # go though all tables and do stuff
    for i in range(0, len(reader)):
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
        if anonymization_type.endswith('FromSet'):
            print('IF')
            referenced_column = get_column_data(protected_column_name)
            anonymized = switch_function(anonymization_type, protectedList, protected_column_name, table_reader, referenced_column)
        else :
            print('ELSE')
            anonymized = switch_function(anonymization_type, protectedList, protected_column_name, table_reader)

        # new table path
        new_table_path = table_path[:-4] + '-anonymized.csv'

        # create new file
        f = open(new_table_path, "w+")
        f.close()

        # write to file
        anonymized.to_csv(new_table_path, index=False)
