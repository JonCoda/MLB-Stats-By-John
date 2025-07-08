from flask import Flask, render_template

# Initialize the Flask application
# __name__ is a special Python variable that tells Flask where to look for resources
# like templates and static files.
app = Flask(__name__)

# Define the route for the homepage ('/')
# When someone visits the root URL of your web application, this function will run.
@app.route('/')
def index():
    # This function renders an HTML template.
    # By default, Flask looks for templates in a folder named 'templates'
    # in the same directory as your app.py file.
    # So, you would need a file named 'index.html' inside a 'templates' folder.
    return render_template('index.html')

# This is a standard Python idiom that ensures the Flask development server
# only runs when the script is executed directly (e.g., `python app.py`),
# not when it's imported as a module into another script.
# The condition should be '__main__', not 'flask'.
if __name__ == '__main__':
    # app.run() starts the Flask development server.
    # debug=True: This enables debug mode, which provides helpful error messages
    #             and automatically reloads the server when you make code changes.
    #             (Remember to set debug=False for production environments!)
    # host='0.0.0.0': This makes the server accessible from other devices on your
    #                 local network, not just your own computer.
    app.run(debug=True, host='0.0.0.0')

