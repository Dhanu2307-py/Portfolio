from flask import Flask,render_template,request,url_for, flash


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

app.secret_key = 'your_secret_key'

# Optional Mail config (commented)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
# app.config['MAIL_PASSWORD'] = 'your_app_password'
# mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Here you can add logic to send an email or store it in a database
        print(f"Message received from {name} ({email}): {message}")
        return render_template('contact.html', success=True)
    return render_template('contact.html', success=False)

if __name__ == '__main__':
    app.run()