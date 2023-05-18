import os
from factory import create_app

app = create_app()

if __name__ == '__main__':
    try:
        print(f"Running app on http://localhost:5001. 🚀🚀")
        # Set the environment variable to enable file monitoring
        os.environ['FLASK_RUN_EXTRA_FILES'] = 'factory/'
        app.run(port=5001, debug=True)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
