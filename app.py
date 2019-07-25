from flask import Flask
from flask import render_template, request, redirect
from boto3.dynamodb.conditions import Key, Attr
import boto3
import json


app = Flask(__name__)

app.DEBUG = True
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/List', methods=['GET', 'POST'])
def list():

    if request.method == 'POST':
        client = boto3.client('lambda')
        key = request.form['key']
        value = request.form['search']
        response=client.invoke(
            FunctionName="hoang-dynamoDB",
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "action": "querryItem",
                "key": key,
                "value": value,
                "name": "Hoang-table"
            }).encode('utf-8')
        )
        rs=json.loads(response['Payload'].read())
        
        return render_template('list.html',student=rs)

    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName="hoang-dynamoDB",
        InvocationType='RequestResponse',
        Payload=json.dumps({
        	"action": "querryTable",
  			"name": "Hoang-table"
		}).encode('utf-8')
    )
    rs=json.loads(response['Payload'].read())
    return render_template('list.html',student=rs)

@app.route('/Add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST'
        msv = request.form['msv']
        name = request.form['name']
        score = request.form['score']
        tp = request.form['type']
        client = boto3.client('lambda')
        student ={
            "MSV": msv,
            "Name": name,
            "Score": score,
            "Type": tp
        }
        rp = client.invoke(
            FunctionName="hoang-dynamoDB",
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "action": "insertTable",
                "name": "Hoang-table",
                "item": student
            }).encode('utf-8')
        )
        rs = json.loads(rp['Payload'].read())
        if rs == "Not complete":
            return render_template('addstudent.html',flag=0)
        else:
            return redirect('/SearchMSV/Result?svalue='+msv)

    return render_template('addstudent.html')
    

@app.route('/Delete')
def delete():
    client = boto3.client('lambda')
    msv = request.args['msv']
    client.invoke(
        FunctionName="hoang-dynamoDB",
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "action": "deleteitem",
            "key": {"MSV":msv},
            "name": "Hoang-table"
        }).encode('utf-8')
    )
    return redirect('/List?')

@app.route('/Edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        msv = request.form['msv']
        name = request.form['name']
        score = request.form['score']
        tp = request.form['type']
        client = boto3.client('lambda')
        student ={
            "MSV": msv,
            "Name": name,
            "Score": score,
            "Type": tp
        }
        client.invoke(
            FunctionName="hoang-dynamoDB",
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "action": "deleteitem",
                "key": {"MSV":msv},
                "name": "Hoang-table"
            }).encode('utf-8')
        )
        client.invoke(
            FunctionName="hoang-dynamoDB",
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "action": "insertTable",
                "name": "Hoang-table",
                "item": student
            }).encode('utf-8')
        )
        return redirect('/List?')    

    client = boto3.client('lambda')
    msv = request.args['msv']
    rp = client.invoke(
        FunctionName="hoang-dynamoDB",
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "action": "getTable",
            "key":{"MSV":msv},
            "name": "Hoang-table"
        }).encode('utf-8')
    )
    rs=json.loads(rp['Payload'].read())
    return render_template('edit.html', result=rs)