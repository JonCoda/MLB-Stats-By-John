from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('webapp.html') 
    
if __name__ == 'flask':
    # Use debug=False in a production environment
    app.run(debug=True, host='0.0.0.0')