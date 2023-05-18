import os

from factory import create_app

app = create_app()

if __name__ == '__main__':
    print(f"Running app. port http://localhost:5001.🚀🚀")
    # Set the environment variable to enable file monitoring
    os.environ['FLASK_RUN_EXTRA_FILES'] = 'factory/'
    app.run(port=5001, debug=True)
