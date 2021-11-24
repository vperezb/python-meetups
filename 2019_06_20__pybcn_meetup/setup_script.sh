virtualenv venv
source venv/Scripts/activate
pip install google-api-python-client httplib2 oauth2client pandas jupyterlab ipykernel
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps google-api-support-vperezb
python -m ipykernel install --user
jupyter lab
