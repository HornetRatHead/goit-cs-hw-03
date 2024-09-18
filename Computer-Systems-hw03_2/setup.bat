@echo off
python -m venv venv
call venv\Scripts\activate.bat
pip install pymongo
pip freeze > requirements.txt