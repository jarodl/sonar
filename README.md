sonar
=====

Sonar monitors different API endpoints for changes. This is still a work in progress and is very much an experiment. The choices for the stack were made for fun over necessity. 

## Items

Adding new end points to monitor should be easy. Here are the current steps:

##### Step 1:

Inherit from BaseItem and override `fetch` to grab the item from an API.

##### Step 2:

Add an `update` in `sonar.py` and schedule its frequency with celery.

##### Step 3:

	TODO: This should probably just be sent as a signal directly from the instance on save

Publish to a juggernaut channel when the item is updated.

##### Step 4:

Add a view and model in `sonar.js` for the item.

## Future

Eliminate as many steps as possible for adding a new item. It would be great if new endpoints could be added on a settings page from the app.

## Development

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