from flask import Flask, render_template, request, redirect
from sqlalchemy.orm import Session
import pandas as pd
from werkzeug.utils import secure_filename
import logging
import sys
import os
import json
from validator import FileChecker
from db.db_schema import Process, ExcelFile, JSONFile
from db.db import DbClient


app = Flask(__name__)

@app.route('/')
def index(name=None):
    db = DbClient()
    with Session(db.engine) as session:
        processes = session.query(Process).all()
        app.logger.info(processes)
    return render_template('index.html', name=name, processes=processes)


@app.route('/process/<id>', methods=['GET'])
def process(id=None):
    db = DbClient()
    with Session(db.engine) as session:
        process = session.query(Process).get(id)
        json_file = session.query(JSONFile).filter(JSONFile.process_id==id)
        excel_files = process.excel_files
        return render_template('process.html', context={'id':id, 'process':process, 'json_file':json_file, 'excel_files':excel_files})

@app.route('/create_process', methods=['POST'])
def create_process(name=None):
    app.logger.info(name)
    app.logger.info(request.form)
    db = DbClient()
    with Session(db.engine) as session:
        process = Process(name=request.form['process_name'])
        session.add(process)
        session.commit()
    return redirect('/')

@app.route('/process/<id>/upload_json', methods=['POST'])
def upload_json(id=None):
    if request.method == 'POST':
        db = DbClient()
        file = request.files['json_filename']
        filename = secure_filename(file.filename)
        filepath = os.path.join('upload', filename)
        file.save(filepath)
        with Session(db.engine) as session:
            process = session.query(Process).get(id)
            json_file = JSONFile(name=filename, path=filepath, process=id)
            session.add(json_file)
            session.commit()
        with open(filepath) as file:
            config = json.loads(file.read())
            app.logger.info(config)
        return redirect('/')


@app.route('/process/<id>/upload_excel', methods=['POST'])
def upload_excel(id=None):
    if request.method == 'POST':
        file = request.files['excel_filename']
        filename = secure_filename(file.filename)
        filepath = os.path.join('upload', filename)
        file.save(filepath)
        db = DbClient()
        with Session(db.engine) as session:
            process = session.query(Process).get(id)
            excel_file = ExcelFile(name=filename, path=filepath, process=id)
            session.add(excel_file)
            session.commit()
        df = pd.read_excel(filepath)
        app.logger.info(df)
        return redirect('/process/' + id)

@app.route('/validate', methods=['GET'])
def validate():
    if request.method == 'GET':
        validator = FileChecker()
        df2 = 'excel_files/test1.xlsx'
        js = 'test1.json'
        v = validator.validate_df(df2, js)
        r = validator.get_response(v)
        app.logger.info(v)
        return r
