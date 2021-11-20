import pandas as pd

def get_dataframe_shape(file_path):
    """
    Эта функция считывает файл и выводит размеры датафрейма
    """
    df = pd.read_csv(file_path)
    return df.shape

def get_dataframe_dtypes(file_path):
    """
    Our function to get dataframe data types  
    """
    df = pd.read_csv(file_path)
    return df.dtypes


def get_dataframe_columns(file_path):
    """
    Our function to get dataframe data types  
    """
    df = pd.read_csv(file_path)
    return df.columns
