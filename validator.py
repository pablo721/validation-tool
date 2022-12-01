import pandas as pd
import json
import datetime
import os

class FileChecker:
    TYPES = {'string': str, 'str': str, 'integer': int, 'int': int, 'decimal': float, 'numeric': float,
                  'float': float, 'date': 'datetime64', 'datetime': 'datetime64', 'timestamp': 'datetime64'}


    def __init__(self):
        self.config = {}
        self.validators = {'integer': self.validate_int, 'int': self.validate_int, 'decimal': self.validate_float,
                      'numeric': self.validate_float, 'float': self.validate_float,
                      'date': self.validate_datetime, 'datetime': self.validate_datetime,
                      'timestamp': self.validate_datetime}


    def get_response(self, validation):
        if validation == True:
            return '<h2><b> File validated successfully. </b></h2>'
        res = '<h2><b> Validation errors: </b></h2>'
        if not validation['extension'][0]:
            res += f'<p> Incorrect file extension - {validation["extension"][1]}.\nAllowed extensions:{self.config["extensions"]}.</p>'
        if validation['unique_together']:
            res += f'<p> Unique together constraint violated by rows: {validation["unique_together"]} </p>'
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


    def validate_extension(self, filepath):
        ext = filepath.split('.')[-1]
        return ext in self.config['extensions'], ext


    def load_config(self, json_file):
        with open(os.path.join(os.getcwd(), 'json_files', json_file)) as cfg:
            self.config = json.loads(cfg.read())


    def validate_df(self, excel_file, json_file):
        res = {}
        self.load_config(json_file)
        print(f'Config: {self.config}')

        df = self.load_file(excel_file)

        for col in df.columns:
            col_config = self.config['cols'][col]
            validation = self.validate_column(df[col], col_config['required'], col_config['unique'], col_config['type'],
                                              col_config['limit'])
            res[col] = validation

        result = 0
        for k, v in res.items():
            for k2, v2 in v.items():
                result += len(v2)

        #print(f'Result: {res}')
        unique_together = []
        if self.config['unique_together']:
            unique_together = self.find_duplicates_df(df[self.config['unique_together']])
            result += len(unique_together)

        valid, ext = self.validate_extension(excel_file)
        if not valid:
            result += 5


        if result == 0:
            return True

        return {'columns': res, 'unique_together': unique_together, 'extension': (valid, ext)}



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
        validator = self.validators[dtype]
        for i, val in column.items():
            print(type(i))
            print(type(val))
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
    def find_duplicates_df(self, df):
        duplicates = df[df.duplicated(keep=False)]
        return list(duplicates.index)

    # finds whole duplicated rows, assuming fields are unique together
    def find_duplicates(self, row):
        duplicates = row[row.duplicated(keep=False)]
        return list(duplicates.index)


    # little polimorphism: string length for strings; max value for numbers; max date for dates
    @staticmethod
    def validate_size(value, max_size, dtype):
        try:
            if 'date' in dtype or dtype == 'timestamp':
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
    def validate_int(value):
        try:
            return value % 1 == 0
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
        min_year = self.config['min_year']
        max_year = self.config['max_year']
        try:
            val = pd.to_datetime(str(value))
            return val.year >= min_year and val.year <= max_year
        except Exception as e:
            return False

if __name__ == '__main__':
    df2 = 'excel_files/test1.xlsx'
    js = 'test1.json'

    v = FileChecker()
    a = v.validate_df(df2, js)
    print(a)
