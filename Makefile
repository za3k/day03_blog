run-debug:
	flask --debug run
run-demo:
	FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=8003 python3 -m flask run
