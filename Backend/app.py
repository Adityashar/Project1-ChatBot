from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('reqpage.html')

@app.route('/submit', methods = ['POST'])
def submit():
	if request.method == 'POST':
		file = request.files['data']
		file.save(file.filename)

	return redirect('/')


if __name__ == '__main__':
	app.run(debug = True)