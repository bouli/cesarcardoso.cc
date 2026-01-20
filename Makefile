build:
	rm -r ./public
	uv run ./main.py

run:
	uv run ./main.py

deploy:
	rm -r ./public/resume/*
	cp -a ../boulihub/cesarcardoso.cc/resume/* ./public/resume
	rm -r ../boulihub/cesarcardoso.cc/*
	cp -a ./public/* ../boulihub/cesarcardoso.cc/
