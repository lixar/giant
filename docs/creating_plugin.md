# Creating a Plugin

## With Help

Lixar Giant includes a handy utility for generating new plugins to aid in making your client or server code generation process as easy as possible. To see the details on generating the plugin, you can run:

    $ giant plugin new -h
    usage: giant plugin new [-h] -t {server,client} -l LANGUAGE -f FRAMEWORK

    optional arguments:
      -h, --help            show this help message and exit
      -t {server,client}, --type {server,client}
                            Whether the plugin will generate a Client or server
      -l LANGUAGE, --language LANGUAGE
                            The name of the language the plugin will generate.
      -f FRAMEWORK, --framework FRAMEWORK
                            The name of the framework the plugin will work with.

If you wanted, for example, to generate a Python Flask server, you could run:

    $ giant plugin new -t client -l Python -f Requests
    Cloning into 'giant-plugin'...
    remote: Counting objects: 35, done.
    remote: Compressing objects: 100% (22/22), done.
    remote: Total 35 (delta 9), reused 35 (delta 9), pack-reused 0
    Unpacking objects: 100% (35/35), done.
    Checking connectivity... done.
    full_name [schapman]: Sandy Chapman
    email [your@email.com]: schapman@lixar.com
    project_language [Python]: 
    project_framework [Requests]: 
    project_type [client]: 
    repo_name [python_requests]: 
    command [python-requests]: 
    help [Generates a Python project using the Requests framework.]: 
    version [0.0.0.1]: 
    copyrightholder [Sandy Chapman]: Lixar I.T.
    description [Generates a Python project using the Requests framework.]: 
    company []: Lixar I.T.
    website []: https://github.com/lixar/giant
    library_name [GiantPlugin]: GiantPythonRequests
    $ 
    
Note, all of the prompts should be optional, however, it's good practice to name these values properly as some of them are used in the generated plugin code.

After running, this, you should have a folder named {lang}_{framework} (in our case `python_requests`) in the current directory. This contains your barebones plugin project. You can now simply start defining your templates in:

    ./python_requests/python_requests/python_requests/templates
    
The heavy nesting is a required feature of Python modules. Once you're ready to use your plugin, go ahead and install it using the following:

    $ giant plugin add -i ./python_requests

This will create a symbolic link to your plugin project, meaning you can make more modifications and then test them out with giant.

    $ giant client python-requests -f ./swagger.yaml -o ./output

## From Scratch

This page will describe how to add an imaginary plugin for a server using the Requests framework written in Python.

Step #1: Create folder

Folders should be named in the form `language-framework-extrainfo`. Often, if the plugin is the first of its kind, the *extra* can be omitted. In our case, we make a folder in the plugins directory named `python-requests`.

Step #2: Create a plugin file

Next, we need to define a plugin file that defines some meta-data for our plugin. This leverages the yapsy plugin file syntax to define our plugin.

Our example is in a file named `python-flask.pirate` looks like this:

    [Core]
    Name = Python Requests Client
    Module = python-requests/python-requests

    [Documentation]
    Author = Your Name
    Version = 0.0.1
    Website = http://yourwebsite.com
    Description = Python Requests Client Generator
    
One thing to note is that the `Module` points to `python-requests/python-requests`. This folder doesn't exist yet, but we'll make it now.

Step #3: Basic Plugin Definition

Add a new folder named `python-flask` inside of `python-flask`.
Inside the outer `python-flask` folder, add a file named `setup.py`. If you're familiar with Python you may be noticing we're simply building a standard Python module.

In your new `setup.py` file, add this code:

    #!/usr/bin/env python

    from setuptools import setup
    setup(
        name = "python-flask",
        version = "1.0",
        packages = ['python_flask'],
    )
    
This defines a basic Python module.

In your `python-flask/python-flask` directory, add another new file named `__init__.py`. Add the following code to it. We'll define the imported class next.

    #!/usr/bin/env python

    from .python_flask import SwaggerPirate

Now add another new file named `python_flask.py` inside the inner `python-flask` directory. In this file, is where we'll define the basic structure of our plugin. A basic plugin looks like the following. It at the minimum defines some plugin meta-data and gives full flexibility to customize the templating engine used by OpenAPI Pirate.

    #!/usr/bin/env python

    import jinja2
    from sapirate_base.sapirate_base import BasePirate
    import os

    class SwaggerPirate(BasePirate):
            
        def plugin_name(self):
            '''Return the name of the plugin.'''
            return 'Python Flask Server'
            
        def plugin_command(self):
            '''Returns a tuple containing:
                * the command line argument to execute the plugin,
                * the help documentation describing the command.'''
            return ('python-flask', 'Generate the Python Flask Server.')

        def loader(self):
            '''Returns the Jinja2 template loader for your templates.'''
            path = os.path.dirname(os.path.realpath(__file__))
            return jinja2.FileSystemLoader(os.path.join(path, 'templates'))

        def helpers_loader(self):
            '''Returns the Jinja2 template loader for your template helpers.'''
            path = os.path.dirname(os.path.realpath(__file__))
            return jinja2.FileSystemLoader(os.path.join(path, 'template-res'))

        def customize_env(self, environment):
            '''Call to allow plugin customization of the Jinja2 environment.'''
            pass
            
        def filters(self):
            '''Call to allow plugin customization of available Jinja2 filters.'''
            pass
                    
        def tests(self):
            '''Call to allow plugin customization of available Jinja2 tests.'''
            pass
            
At this point, you should have a basic plugin working. You can test your work by running the following command and observing the output:

    $ ./pirate.py --help
    usage: pirate.py [-h]
                      {...,python-flask,...}
    ...
            
The last step is to define your templates. Create a new folder named `templates` in `python-flask/python-flask`. Add the following file named `controller.py.jinja` to it:

    #!/usr/bin/env python

    from flask import Flask
    app = Flask(__name__)

    {% for operation_name, operation in operations.iteritems() %}
    @app.route('{{ operation.path_name }}', methods=['{{ operation.method|upper }}'])
    def {{ operation_name }}(\*args, \*\*kwargs):
        return '{{ operation_name }}'
    {% endfor %}

    if __name__ == "__main__":
        app.run()
        
If you know, flask, this will look somewhat familiar to you. The difference is we're using Jinja2 templating to iterate over all of the Swagger operations to produce a controller endpoint for each one.

Pirate offers some help when navigating Swagger documents such as a nice operations based interface which make iterate less cumbersome than starting at a path and moving down. Operations have a back link to the path they belong to, as well, as their method and name which we make use of in the example above.

If you generate the client at this point, you'll get something very close to a work output. However, the endpoints look like this:

    @app.route('/coffee/{coffeeId}', methods=['PUT']')
    def updateCoffeeOrder(\*args, \*\*kwargs):
      return None
      
Notice that the path uses `{` and `}`, when Flask requires '<' and '>' to denote path variables. Let's write a filter to fix this. In your `python_flask.py` file, add the following import to the top of the file:

    from .filters import filters
    
And replace the `pass` in the `filters` method to `return filters()`.
    
Then, create a new file named `filters.py` in the `python-flask/python-flask` directory and add the following code:

    #!/usr/bin/env python

    def \_swagger_path_to_flask_path(path):
        return path.replace('{','<').replace('}', '>')

    def filters():
        return (
            ('swagger_path_to_flask_path', \_swagger_path_to_flask_path),
        )
        
This defines new methods `_swagger_path_to_flask_path` and `filters`. We're exposing `filters` to `python_flask.py` via the import we added above. This will define a filter we can use in Jinja named `swagger_path_to_flask_path`.

Now, change this line in our `controller.py.jinja` template from this:

    @app.route('{{ operation.path_name }}', methods=['{{ operation.method|upper }}'])
    
to this:

    @app.route('{{ operation.path_name|swagger_path_to_flask_path }}', methods=['{{ operation.method|upper }}'])
    
And regenerate your code:

    @app.route('/coffee/<coffeeId>', methods=['PUT']')
    def updateCoffeeOrder(\*args, \*\*kwargs):
        return None
        
That's better. Let's run the app:

    $ pip install flask
    $ chmod 755 python-flask/controller.py
    $ ./python-flask/controller.py
    \* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Then use your favourite REST client to test it (e.g. Postman):

    $ curl -X GET "http://127.0.0.1:5000/coffee"
    listCoffees

Voila! You can take it from here.
            
        
