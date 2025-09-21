# Makefile

ENV_NAME = JMTA

update-reqs:
	pip freeze > requirements.txt
