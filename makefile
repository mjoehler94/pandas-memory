install:
	- pip install --upgrade pip && pip install -r requirements.txt 

uninstall:
	- pip freeze > temp.tmp && pip uninstall -r temp.tmp -y && rm temp.tmp
