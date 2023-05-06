from flask import Flask, render_template, request,url_for
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume.pdf')
def resume():
    return app.send_static_file('resume.pdf')

@app.route('/save', methods=['POST'])
def save():
    data = request.form['data']
    with open('eye_tracking_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data])
    return ''

if __name__ == '__main__':
    app.run(debug=True)
