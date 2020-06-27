from flask import Flask, render_template, request, redirect
from dataload import loadData
import os
from voicebotfunc import talk
app = Flask(__name__)

strs = []
@app.route('/')
def hello():
	return render_template('index.html', lis = strs, length = len(strs))

@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        file = request.files['data']
        file.save(file.filename)
        loadData(file.filename)
        q = 'python Backend/dynamictrain.py ' + file.filename
        os.system(q)
        os.system('python Backend/train.py')

    return redirect('/')

@app.route('/mike', methods = ['POST'])
def mike():
    if request.method == 'POST':

        message, botmessage = talk()


        strs.append(message)
        strs.append(botmessage)
        
        return redirect('/')
        #loadtheModule(file.filename, file.filename)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True)
