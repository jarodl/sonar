sonar
=====

Welcome to Sonar. Sonar uses Flask and Celery to schedule fetches for new content related to MindSnacks. Juggernaut uses Redis to pass messages to the client when new content is available. It's pretty much the trendiest project ever.

Development
-----------

	mkvirtualenv sonar
	
	# needed for gevent
	brew install libevent
	# needed for juggernaut
	brew install redis

	npm install -g juggernaut

	pip install -r requirements.txt

	gem install foreman

	# start redis
	redis-server

	# start juggernaut
	juggernaut

	# start celery
	python sonar/manager.py celeryd -B

	# start sonar
	foreman start

Check [localhost:5000](http://localhost:5000)