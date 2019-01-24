#!/usr/bin/python3.6

import os.path
import os, fnmatch
import re, sys
import subprocess
from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from flask_autoindex import AutoIndex

print (sys.argv);
dir = sys.argv[1]
ocr = 0

################################################################################
class Counter:
  def __init__(self):
    self.dict = {}
  def add(self,item):
    count = self.dict.setdefault(item,0)
    self.dict[item] = count + 1
  def counts(self,desc=None):
    result = [[val, key] for (key, val) in self.dict.items()]
    result.sort()
    if desc: result.reverse()
    return result
################################################################################

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = dir + "/Scan"

# 30 MB upper limit on uploaded files
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

################################################################################
# upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return ""
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

################################################################################
# q: Query
@app.route("/q/")
def find():
  find=request.args.get('q', 0, type=str)
  find=find.split(' ')
  c=Counter()
  found=[]
  for path, dirs, files in os.walk(os.path.abspath(dir)):
    for filename in fnmatch.filter(files, '*.txt'):
      filepath = os.path.join(path, filename)
      with open(filepath) as f:
        alines = f.readlines();
        alines = " ".join(alines);
        if all(i.lower() in alines.lower() for i in find):
          c.add(path.replace(dir + "/", '/'))
  for i in c.counts(1):
    found.append(i[1])
  for path in found:
    print (path)
  return render_template('result.html', found=found)

################################################################################
# import: import new documents
@app.route("/import")
def imp():
  here = os.path.dirname(__file__) + "/ocr " + dir + "/Scan"
  print (here)
  ocr = subprocess.Popen([here], stdout = subprocess.PIPE, shell=True)
  return ""

################################################################################
# state: import new documents
@app.route("/state")
def state():
  imp();
  f = open(dir + "/Scan/state", "r")
  state = f.read();
  f.close();
  state = state.strip()
  if state != "":
    state = state + "<br/><br />"
  return state

################################################################################
@app.route('/')
@app.route('/index.html')
def index():
  return render_template('index.html')

################################################################################
AutoIndex(app, browse_root=dir)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
