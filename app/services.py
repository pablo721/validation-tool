import pandas as pd
import json
import os
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide
from .models import Process, UniqueTogetherColumns, DataColumn
from .db import DbClient



class ValidationService:
    TYPES_DICT = {'string': 'str', 'str': 'str', 'integer': 'int', 'int': 'int', 'decimal': 'float', 'numeric': 'float',
                  'float': 'float', 'date': 'datetime64', 'datetime': 'datetime64', 'timestamp': 'datetime64'}
    EXTENSIONS = ['xls', 'xlsx', 'csv']
    DTYPES_DICT = {1: 'str', 2: 'int', 3: 'float', 4: 'date'}

    def __init__(self):
        self.config = {}
        self.validators = {'int': self.validate_int, 'float': self.validate_float, 'datetime64': self.validate_datetime}

    @staticmethod
    def find_invalid_columns(df, columns):
        invalid = []
        proc_cols = [col.name.lower() for col in columns]
        for col in df.columns:
            if col.lower() not in proc_cols:
                invalid.append(col)
        return invalid

    def validate_df2(self, excel_filepath, process, columns, unique_together: list[str]):
        res = {}
        result = 0
        errors = []

        if not excel_filepath:
            errors.append('No excel file.')
        if not process:
            errors.append('No process specified.')

        valid, ext = self.validate_extension(excel_filepath)

        if not valid:
            errors.append(f'Invalid file extension - {ext} is not supported.')

        proc_col_names = [col.name for col in columns]
        df = self.load_file(excel_filepath)
        invalid_cols = self.find_invalid_columns(df, columns)
        if mismatched_cols:
            errors.append(f'Invalid columns: {invalid_cols}.\nValid columns for process {process.name} are: {proc_col_names}')

        if errors:
            return {'errors': errors}


        for col_name in df.columns:
            column = self.find_column(col_name, columns)
            validation = self.validate_column(df[col_name], column.required, column.unique,
                                              self.DTYPES_DICT[column.dtype_id], column.max_size)
            res[col] = validation

        for k, v in res.items():
            for k2, v2 in v.items():
                result += len(v2)

        if unique_together:
            unique_together = self.find_duplicates(df[unique_together])
            result += len(unique_together)

        result += len(errors)

        if result == 0:
            return True

        return {'columns': res, 'errors': errors, 'unique_together': unique_together}

    @staticmethod
    def find_column(col_name, columns):
        for col in columns:
            if col.name.lower() == col_name.lower():
                return col

    def get_response(self, validation):
        if validation == True:
            return '<h2><b> File validated successfully. </b></h2>'
        res = '<h2><b> Validation errors: </b></h2>'
        if 'errors' in validation.keys():
            for error in validation['errors']:
                res += f'<p> {error}.\n</p>'
        if 'unique_together' in validation.keys():
            res += f'<p> Unique together constraint violated by rows: {validation["unique_together"]} </p>'

        if 'columns' in validation.keys():
            for name, col in validation['columns'].items():

                res2 = f'<h4><b> Column: {name} </b></h4>'
                for k, v in col.items():
                    if v:
                        res2 += f'<p> {k}: rows {v}</p>'
                res += res2
                res += '<br>'
        return res

    @staticmethod
    def load_file(filepath):
        ext = filepath.split('.')[-1]
        if ext == 'csv':
            return pd.read_csv(filepath)
        if 'xls' in ext:
            return pd.read_excel(filepath)
        return 'Invalid extension.'

    def validate_extension(self, filepath):
        ext = filepath.split('.')[-1]
        return ext in self.EXTENSIONS, ext



    def load_process(self, process_name, process_id=None):
        with Session(self.db_client) as session:
            if process_name:
                process = session.query(Process).filter(name=process_name).first()
            elif process_id:
                process = session.query(Process).filter(id=process_id).first()
            else:
                return 'Please provide either process name or process id.'

            if not process:
                return 'Process does not exist.'
            return process

    # def find_unique_together(self, process):
    #     with Session(self.db_client) as session:
    #         unique_together = session.query(UniqueTogetherColumns).filter(process_id=process.id)
    #         print(f'Process id: {process_id}, unique together: {unique_together}')
    #         return unique_together



    def validate_column(self, column, required, unique, dtype, max_size):
        res = {}
        if required:
            res['Nulls'] = self.find_nulls(column)
        if unique:
            res['Duplicates'] = self.find_duplicates(column)

        res['Invalid data types'] = self.validate_column_dtypes(column, dtype)
        res['Invalid size'] = self.validate_column_sizes(column, max_size, dtype)
        return res

    def validate_column_sizes(self, column, max_size, dtype):
        res = []
        for i, val in column.items():
            if not self.validate_size(val, max_size, dtype):
                res.append(i)
        return res

    def validate_column_dtypes(self, column, dtype):
        res = []
        validator = self.validators[self.TYPES_DICT[dtype]]
        for i, val in column.items():
            if not validator(val):
                res.append(i)
        return res

    def validate_unique_together(self, df, cols):
        return self.find_duplicates(df[cols])


    def find_nulls(self, row):
        nulls = row[row.isna()]
        return list(nulls.index.values)


    def find_nulls_df(self, df):
        res = {}
        nulls = df.isna().any(axis=1)
        if len(nulls) == 0:
            return True
        indexes = [idx for idx, val in nulls.items() if val]
        for i, row in df.loc[indexes].iterrows():
            res[i] = [col_name for col_name, value in row.items()]
        return res



    # finds whole duplicated rows, assuming fields are unique together
    def find_duplicates(self, data):
        duplicates = data[data.duplicated(keep=False)]
        return list(duplicates.index)


    # little polimorphism: string length for strings; max value for numbers; max date for dates
    @staticmethod
    def validate_size(value, max_size, dtype):
        try:
            if dtype == 'datetime64':
                print(pd.to_datetime(str(value)).timestamp())
                return pd.to_datetime(str(value)).timestamp() <= max_size

            elif 'str' in dtype:
                return len(value) <= max_size
            else:
                val2 = float(value)
                return val2 <= max_size
        except Exception as e:
            return True


    @staticmethod
    def validate_str(value):
        try:
            str(value)
            return True
        except Exception as e:
            return False

    @staticmethod
    def validate_int(value):
        try:
            return float(value) % 1 == 0
        except Exception as e:
            return False

    @staticmethod
    def validate_float(value):
        try:
            float(value)
            return True
        except Exception as e:
            return False


    def validate_datetime(self, value):
        try:
            pd.to_datetime(str(value))
            return True
        except Exception as e:
            return False


if __name__ == '__main__':
    df2 = 'excel_files/test1.xlsx'
    js = 'test1.json'

    v = ValidationService()
    a = v.validate_df(df2, js)
    print(a)
