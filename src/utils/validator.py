import pandas as pd
from pathlib import Path
from typing import Tuple

def validate_csv(template: pd.DataFrame, dataset: pd.DataFrame, primary_keys: list = [],
                 imagepath_column_name: str = None, non_nan_columns: list = []) -> Tuple[bool, str]:
    """ Comparing a csv file to a gold standard template.

        Checks if a dataset:
        (1) has same and all columns compared to template?
        (2) has unique primary keys?
        (3) contains only valid image file paths i.e. all paths pointing to a file on disk.
        (4) does not contain NaNs
    """

    # (1) Check if all column names of template are columns names in dataset
    if not all(elem in list(dataset.columns) for elem in list(template.columns)):
        # Find missing elements of dataset
        missing_elems = [elem for elem in list(template.columns) if elem not in list(dataset.columns)]
        error_str = ""
        # Check if element is optional
        for elem in missing_elems:
            # Get first row of a given column.
            if template[elem].iloc[0].lower().strip() != "optional":
                error_str += f"Dataset not valid due to missing mandatory column in provided dataset. Missing column: '{elem}'"
        if len(error_str) > 0:
            return False, error_str
    print(
        f"Successfully verified that all mandatory column names are present in provided dataset. Column names: {list(template.columns)}")

    # (2) Check if primary keys are unique
    if primary_keys is not None and isinstance(primary_keys, list) and len(primary_keys) > 0:
        are_primary_keys_unique = is_unique(keys=primary_keys, dataset=dataset)
        if not are_primary_keys_unique[0]: return are_primary_keys_unique
    print(f"Successfully verified that primary keys are unique in provided dataset. Primary keys: {primary_keys}")

    # (3) Check if all images in dataset point to a existing file on disk.
    if imagepath_column_name is not None:
        is_file_valid = is_file(path_list=dataset[imagepath_column_name].tolist())
        if not is_file_valid[0]: return is_file_valid
    print(f"Successfully verified that all images in dataset point to a existing file on disk.")

    # (4) Check if there are any NaN values in specified non-NaN columns.
    if non_nan_columns is not None and isinstance(non_nan_columns, list) and len(non_nan_columns) > 0:
        is_not_nan_result = is_not_nan(columns=non_nan_columns, dataset=dataset)
        if not is_not_nan_result[0]: return is_not_nan_result
    print(
        f"Successfully verified that there are no NaN values in the specified non-NaN columns. non-NaN columns: {non_nan_columns}")

    # TODO: Add further validation functions here.
    # (5)

    return True, "No error detected. Dataset is valid."


def is_not_nan(columns: list, dataset: pd.DataFrame) ->Tuple[bool, str]:
    df_select_colums = dataset.loc[:, columns]
    number_of_nans = df_select_colums.isnull().sum().sum()
    if number_of_nans > 0:
        return False, f"There are {number_of_nans} NaNs or undefined values present in the dataset's columns {columns}. Please revise."
    return True, ""


def is_unique(keys: list, dataset: pd.DataFrame) ->Tuple[bool, str]:
    # Method 1: Comparing shapes after dropping duplicates
    df_shape_with_dups = dataset.shape[0]
    df_shape_without_dups = dataset[keys].drop_duplicates().shape[0]
    if not df_shape_with_dups == df_shape_without_dups:
        # Method 2: Raising value error via pd.set_index with verify_integrity==True to raise an interpretable error
        try:
            dataset[keys].set_index(keys, verify_integrity=True)
        except Exception as e:
            return False, str(e)
    return True, ""


def is_file(path_list: list, max_num_exceptions: int = 100) ->Tuple[bool, str]:
    error_str = ""
    exception_counter = 0
    # disable_tqdm = False if len(path_list) > 2 else True
    # pbar = tqdm(path_list, disable=disable_tqdm)
    for path in path_list:
        # pbar.set_description(f"Checking if images files exist..")
        try:
            assert Path(
                path).is_file(), f"The path you provided '{path}' does not point to a valid file. Please revise and try again. "
        except Exception as e:
            # error string should include all errors to avoid having to rerun the script several times.
            error_str += str(e) + "\n"
            exception_counter += 1
            # let's add some early stopping here to avoid waiting a long time if none of the files is found.
            if exception_counter >= max_num_exceptions: break
    if exception_counter > 0:
        return False, error_str
    else:
        return True, error_str
