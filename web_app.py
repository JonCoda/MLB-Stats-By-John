from flask import Flask, render_template

app = Flask(webapp)

@app.route('/')
def index():
    return render_template('web_app.html')
    
if __name__ == 'webapp':
    # Use debug=False in a production environment
    app.run(debug=True, host='0.0.0.0')
