# Lixar Giant

## <a name="top"></a>Contents

* [Overview](#overview)
* [Requirements](#requirements)
* [Quick Setup](#quick-setup)
* [Code Examples](#code-examples)
  * [Servers](#servers)
    * [C# Web API 2.0](csharp-webapi)
  * [Clients](#clients)
    * [Swift iOS](#swift-ios)
    * [Java Android](#java-android)
* [Reference / Help](#help)
* [Contributors](#contributors)
* [Authors](#authors)
* [License](#license)

## <a name="overview"></a>Overview [<sub><sub>top</sub></sub>](#top)

Lixar Giant is a code generation tool for OpenAPI (Swagger 2.0) Specification documents. It's written in *Python* and designed for extensibility.

It aims to be a simple and quick way to generate both clients and servers for your API project.

## <a name="requirements"></a>Requirements [<sub><sub>top</sub></sub>](#top)

**Python** - Used for executing the tool.

**pip** - The Python package tool for installing dependencies.

**virtualenvwrapper** (recommended) - Used for isolating project environment.

## <a name="quick-setup"></a>Quick Setup [<sub><sub>top</sub></sub>](#top)

\*\*\**Note: PYPI install coming soon!*\*\*\*

##### 1. Checkout Code

    $ git clone git@github.com:lixar/giant.git
    
##### 2. (Optional) Activate a virtualenv.

    $ mktmpenv -n
    
##### 3. Install (tip: use `sudo` if installing without an virtualenv)

    $ pip install ./giant
    
##### 4. Generate some code

    $ giant server webapi -f ./swagger.yaml -o ./webapi

## <a name="code-examples"></a>Code Examples [<sub><sub>top</sub></sub>](#top)

### <a name="servers"></a>Servers [<sub><sub>top</sub></sub>](#top)

#### <a name="csharp-webapi"></a>C# Web API 2.0

    $ giant csharp-webapi -f ./swagger.yaml -o ./csharp-webapi
    
### <a name="clients"></a>Clients [<sub><sub>top</sub></sub>](#top)

#### <a name="swift-ios"></a>Swift iOS

    $ giant swift-ios -f ./swagger.yaml -o ./swift-ios

#### <a name="java-android"></a>Java Android

    $ giant java-android -f ./swagger.yaml -o ./java-android

## <a name="help"></a>Reference / Help [<sub><sub>top</sub></sub>](#top)

Lixar Giant has help built in. To list the available plugins, run:

    $ giant --help
    
You'll get something looking like this:

    giant --help
    usage: giant [-h] {android,ios,webapi} ...

    Generate code from swagger.

    positional arguments:
    {android,ios,webapi}  Swagger project to generate. Use "$ giant
                        [command] --help" for more details on command usage.
    android             Generate the Android swagger client.
    ios                 Generate the iOS swagger client.
    webapi              Generate the ASP.NET Web API stub server.

    optional arguments:
    -h, --help            show this help message and exit
    
To get help on a specific plugin, specify the name before the `--help`:

    $ giant webapi --help
    usage: giant webapi [-h] [-u SWAGGER_URL]
                            [-f SWAGGER_FILES [SWAGGER_FILES ...]]
                            [-m SWAGGER_META] [-o OUTPUT_DIR]

    optional arguments:
      -h, --help            show this help message and exit
      -u SWAGGER_URL, --url SWAGGER_URL
                            The URL of the remote swagger file.
      -f SWAGGER_FILES [SWAGGER_FILES ...], --swagger-files SWAGGER_FILES [SWAGGER_FILES ...]
                            The path of the local swagger file.
      -m SWAGGER_META, --swagger-metadata SWAGGER_META
                            The path of the local swagger metadata file.
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            The output directory for generated files.
    

## <a name="contributors"></a>Contributors [<sub><sub>top</sub></sub>](#top)

We're wide open to contributions. Just open a pull request for any code contributions, or submit a patch to [schapman@lixar.com](mailto:schapman@lixar.com). Please use the Wiki to open any bug reports or suggested improvements.

### Creating a Plugin

See [Creating a Plugin](url-here).

## <a name="authors"></a>Authors [<sub><sub>top</sub></sub>](#top)

Software by **[Lixar I.T. Inc.](http://lixar.com/)**

* Sandy Chapman - [schapman@lixar.com](mailto:schapman@lixar.com)
* Ricardo Santos - [rsantos@lixar.com](mailto:rsantos@lixar.com)
* Marcel Farcas - [mfarcas@lixar.com](mailto:mfarcas@lixar.com)

## <a name="license"></a>License [<sub><sub>top</sub></sub>](#top)

The MIT License (MIT)

Copyright © 2016 Lixar I.T. Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.