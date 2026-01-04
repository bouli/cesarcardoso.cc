build:
	rm -r ./public
	uv run ./main.py

run:
	uv run ./main.py

deploy:
	rm -r ../boulihub/cesarcardoso.cc/*
	cp -a ./public/* ../boulihub/cesarcardoso.cc/
