#!/usr/bin/env python

"""Description goes here"""

import webbrowser
import argparse
import os
from flask import Flask, request, render_template, jsonify

DEFAULT_HOST = '127.0.0.1'
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(BASE_PATH, 'templates')
STATIC_DIR = os.path.join(BASE_PATH, 'static')
DEFAULT_PORT = 5000

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


@app.route('/')
def index():
    """Render the main index"""
    return render_template('index.pug')


def get_extra_files():
    """returns a list of files that should be watched by the Flask server
    when in debug mode to trigger a reload of the server
    """
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    extra_dirs = [THIS_DIR]
    extra_files = []
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename) and filename not in extra_files:
                    extra_files.append(filename)
    return extra_files


def main():
    """Entry point from command line"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--debug', help='The debug flag of this Flask application.', action='store_true')
    parser.add_argument('--host', help='The host ip address on which gdbgui serve. Defaults to %s' % DEFAULT_HOST, default=DEFAULT_HOST)
    parser.add_argument('-p', '--port', help='The port on which gdbgui will be hosted. Defaults to %s' % DEFAULT_PORT, default=DEFAULT_PORT)

    # templates are written in pug, so add the pypugjs extension
    app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

    args = parser.parse_args()

    if args.debug:
        extra_files = get_extra_files()
    else:
        extra_files = []
        webbrowser.open('http://%s:%s' % (args.host, args.port))

    app.run(debug=args.debug, host=args.host, port=args.port, extra_files=extra_files)


if __name__ == '__main__':
    main()
