run-debug:
	flask --debug run
run-demo:
	gunicorn3 -e SCRIPT_NAME=/hackaday/blog --bind 0.0.0.0:8003 app:app
	#FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=8003 python3 -m flask run
