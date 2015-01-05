WHAuth
======

An Authentication and Authorization system for wormhole corps/alliances within EVE Online

Heavily in development at the current time.

Developing in Python 3.4

Rename config.dist.py to config.py, edit the variables as required.

Requirements can be found in requirements.txt, run the debug server with run_debug.py.

## Install

Installing currently requires that your system have the Python development headers, and libffi's development headers.

In debian-based systems you can install the required packages with this command:
```
sudo apt-get install python3-dev build-essential libffi-dev
```

Also, You need to have node.js and npm installed, to be able to install Bower:
```
sudo npm install -g bower
```

Next, set up and activate your virtualenv for Auth (note we're specifying python3 here):
```
virtualenv -p $(which python3) env
source env/bin/activate
```

Install all the requirements of WHAuth
```
pip install -r requirements.txt
bower install
```

Finally, rename the configuration file to config.py and edit to your liking:
```
cp config.dist.py config.py
```
