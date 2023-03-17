from flask import Flask, render_template, request, redirect, current_app
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import Session
import pandas as pd
from werkzeug.utils import secure_filename
from logging import Logger
import os
import json
from .models import Process, DataColumn, DataType, UniqueTogetherColumns
from .db import DbClient
from .services import ValidationService
from .utils import parse_process_cols
from .containers import Container
from .settings import FILES_DIR


@inject
def index(db_client: DbClient = Provide[Container.db_client]):

    with Session(db_client.engine) as session:
        processes = session.query(Process).all()

    return render_template('index.html', processes=processes)


@inject
def process(proc_id,  db_client: DbClient = Provide[Container.db_client]):
    with Session(db_client.engine) as session:
        process = session.query(Process).filter(Process.id == proc_id).first()
        current_app.logger.info(process.id)
        #excel_files = process.excel_files
        return render_template('process.html', proc_id=proc_id, process=process)

#@app.route('/process/new', methods=['GET'])
@inject
def new_process():
    return render_template('new_process.html')

#@app.route('/create_process', methods=['POST'])
@inject
def create_process(db_client: DbClient = Provide[Container.db_client]):
    form = request.form.to_dict()
    process_name = form.pop('new_process_name')
    if not process_name:
        return 'Please provide process name.'
    file_name = form.pop('new_process_file_name')

    cols = parse_process_cols(form)

    with Session(db_client.engine) as session:
        process = Process(name=process_name, file_name=file_name, file_ext=file_name.split('.')[-1])
        session.add(process)
        unique_together_cols = []
        for n, rules in cols.items():
            current_app.logger.info(rules)
            dtype_id = session.query(DataType).filter(DataType.name == rules['dtype']).first().id
            column = DataColumn(name=rules['attribute_name'], process_id=process.id, dtype_id=dtype_id,
                                max_size=rules['max_size'])
            session.add(column)

            if 'required' in rules.keys():
                column.nullable = True
            if 'unique' in rules.keys():
                column.unique = True
            if 'unique_together' in rules.keys():
                unique_together_cols.append(column.name)

        session.commit()

    with Session(db_client.engine) as session:
        process = session.query(Process).filter(Process.name == process_name).first()
        for col_name in unique_together_cols:
            unique_obj = UniqueTogetherColumns(process_id=process.id, column_name=col_name)
            session.add(unique_obj)

        session.commit()

    return redirect('/')
@inject
def validate(proc_id, validation_service: ValidationService = Provide[Container.validation_service],
             db_client: DbClient = Provide[Container.db_client]):

        with Session(db_client.engine) as session:
            process = session.query(Process).get(proc_id)
            columns = session.query(DataColumn).filter(DataColumn.process_id == proc_id).all()
            unique_together = session.query(UniqueTogetherColumns).filter(DataColumn.process_id == proc_id)
            excel_filepath = os.path.join(FILES_DIR, process.file_name)
            current_app.logger.info('columnsDASDASDSADSADSADADSADSA')
            current_app.logger.info(columns)

            v = validation_service.validate_df2(excel_filepath, process, columns, unique_together)
            r = validation_service.get_response(v)

            return r
@inject
def upload(proc_id, db_client: DbClient = Provide[Container.db_client]):
    with Session(db_client.engine) as session:
        process = session.query(Process).get(proc_id)
        current_app.logger.info(process.file_name)
        file = request.files['excel_filename']
        filename = secure_filename(file.filename)
        filepath = os.path.join('app', 'excel_files', filename)
        file.save(filepath)
        process.file_name = filename
        session.commit()
        return redirect('/process/' + proc_id)


#@app.route('/process/<id>/upload_json', methods=['POST'])
# def upload_json(id=None):
#     if request.method == 'POST':
#         db = DbClient()
#         file = request.files['json_filename']
#         filename = secure_filename(file.filename)
#         filepath = os.path.join('../old/upload', filename)
#         file.save(filepath)
#         with Session(db.engine) as session:
#             process = session.query(Process).get(id)
#             json_file = JSONFile(name=filename, path=filepath, process=id)
#             session.add(json_file)
#             session.commit()
#         with open(filepath) as file:
#             config = json.loads(file.read())
#             app.logger.info(config)
#         return redirect('/')
#
#
# #@app.route('/process/<id>/upload_excel', methods=['POST'])
#
#
# #@app.route('/validate', methods=['GET'])
