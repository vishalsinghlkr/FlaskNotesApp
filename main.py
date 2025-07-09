from website import create_app #import from the website package __init__.py file
app=create_app() #call the create_app function to create the Flask app instance
if __name__ == '__main__': # Check if this script is run directly
    app.run(debug=True)  # Run the app in debug mode for development
    