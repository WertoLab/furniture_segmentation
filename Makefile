debug:
	docker-compose up --build --force-recreate --remove-orphans

up:
	docker-compose up --build -d --force-recreate

down:
	docker-compose down

local: # poetry run
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
	#uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# poetry export -f requirements.txt -o requirements.txt --without-hashes

init_env:
	cp ./.env.example ./.env
