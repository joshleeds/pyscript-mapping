import pandas as pd
import numpy as np
from js import document, FileReader, console #Blob, URL, 
from io import StringIO, BytesIO
from pyodide.ffi import create_proxy

console.log("Script loaded and running...")

def handle_upload(event):
    console.log("Uploading file...")
    file = document.getElementById('excel-upload').files.item(0)
    reader = FileReader.new()

    def combine(event):
        file_content = event.target.result
        
        # reads the file as either a CSV or Excel file depending on the file extension most likely will be a Excel
        if file.name.endswith('.csv'):
             df = pd.read_csv(StringIO(file_content.decode('utf-8')))
        elif file.name.endswith(('.xls', '.xlsx')):
            binary_data = memoryview(file_content.to_py())  # 🔥 convert JsProxy to Python bytes-like object
            df = pd.read_excel(BytesIO(binary_data), sheet_name=0)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        
        ###Combining of the data
        console.log("Data read")
        # Keep only the specified columns
        # required_columns = ['Date', 'Description', 'Paid Out', 'Balance', 'Classification']
        # df = df[required_columns]
        training_data = df[df['Classification'].notnull()]
        training_data = training_data.dropna()

        class_map = dict(zip(training_data['Description'], training_data['Classification']))
        df['Classification'] = df['Classification'].fillna(df['Description'].map(class_map))

        count_null = df['Classification'].isnull().sum()
        console.log(f"Number of null values in Classification column: {count_null}")
        console.log(f"Number of rows in the data: {df.shape[0]}")


    #  Create proxy so Pyodide doesn’t destroy it
    reader.onload = create_proxy(combine)
    reader.readAsArrayBuffer(file)

# Also wrap the outer handler in a proxy
document.getElementById("process-btn").addEventListener("click", create_proxy(handle_upload))

