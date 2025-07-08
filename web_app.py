from flask import app, render_template

app = ('webapp.html') 

@app.route('/')
def index():
    return render_template(app) 
    
if __name__ == 'webapp.html':
    # Use debug=False in a production environment
    app.run(debug=True, host='0.0.0.0')