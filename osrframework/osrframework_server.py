#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##################################################################################
#
#    Copyright 2017 Félix Brezo and Yaiza Rubio (i3visio, contacto@i3visio.com)
#
#    This program is part of OSRFramework. You can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################

__author__ = "Felix Brezo y Yaiza Rubio "
__copyright__ = "Copyright 2015-2017, i3visio"
__credits__ = ["Felix Brezo", "Yaiza Rubio"]
__license__ = "AGPLv3+"
__version__ = "v0.0.3"
__maintainer__ = "Felix Brezo, Yaiza Rubio"
__email__ = "contacto@i3visio.com"


import argparse
import json
import os
import time
import shlex
import sys

# Server code
import flask
from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template

# OSRFramework libraries
import osrframework
import osrframework.domainfy as domainfy
import osrframework.entify as entify
import osrframework.mailfy as mailfy
import osrframework.phonefy as phonefy
import osrframework.searchfy as searchfy
import osrframework.usufy as usufy

import osrframework.utils.configuration as configuration
from osrframework.utils.daemon import Daemon


# Initiliazing the SECRET TOKEN
SECRET_TOKEN = ""

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
    return render_template('home.html', mt_home='class=current')

@app.route("/research")
@app.route("/research/<program>")
def research(program=None):
    if not program:
        return render_template('research.html', mt_research='class=current', mr_main='class=current')
    else:
        params = request.args.get('query_text')
        return render_template('research-' + program + '.html', mt_research='class=current', query_text=params)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['csv'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/explore", methods=['GET', 'POST'])
def explore():
    # Based on http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            notice = {
                "icon": "warning",
                "message": "No file was selected." ,
                "type": "warning"
            }
            return render_template('explore.html', mt_explore='class=current', alert=notice)

        # Checking if the file name is permitted
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # TODO: pretty unsafe as it is now
            # Recovering the loadedData: !
            global loadedData
            loadedData["csv"] = ""
            everything = file.stream.read().splitlines()
            for i, line in enumerate(everything):
                loadedData["csv"] += line
                # Checking if it is the last line. This is done to avoid extra lines.
                if i+1 != len (everything):
                    loadedData["csv"] += "\n"

            return render_template('explore.html', mt_explore='class=current', csvData=loadedData["csv"])
        else:
            notice = {
                "icon": "close",
                "message": "This is not a valid extension. We only support CSV files.",
                "type": "error"
            }
            return render_template('explore.html', mt_explore='class=current', alert=notice)
    else:
        return render_template('explore.html', mt_explore='class=current')


<<<<<<< HEAD
@app.route("/info")
def getInfo():
    info = {
        "__version__": "OSRFramework " + osrframework.__version__,
        "license": "AGPLv3",
        "server_time": _getServerTime()[1],
        "source_code": "https://github.com/i3visio/osrframework",
    }
    return flask.Response(
        json.dumps(
            info,
            indent=2,
            sort_keys=True
        ),
        status=200,
        mimetype="application/json"
=======

@app.route('/research/<program>', methods=['POST'])
def run(program):
    """Loading OSRFramework output...
    """
    # Grabbing the text search...
    strParams = request.form['tex_command']

    if strParams != None:
        # Splitting the query
        params = shlex.split(strParams)

        # Selecting the appropriate program
        if program == "domainfy":
            args = domainfy.getParser().parse_args(params)
        elif  program == "entify":
            args = entify.getParser().parse_args(params)
        elif program == "mailfy":
            args = mailfy.getParser().parse_args(params)
        elif program == "phonefy":
            args = phonefy.getParser().parse_args(params)
        elif program == "searchfy":
            args = searchfy.getParser().parse_args(params)
        elif program == "usufy":
            args = usufy.getParser().parse_args(params)
            print args
        # Return output. text/html is required for most browsers to show the text
        answer = runQuery(program=program, args=args)
    else:
        pass
        answer = {}

    return render_template(
        'research-' + program + '.html',
        mt_research='class=current',
        text_results=general.usufyToTextExport(answer)
>>>>>>> 162017d... Remove current mark after performing a search
    )


# --------------
# API Management
# --------------


@app.route('/api/v1/<command>/<query>')
def api_v1(command, query):
    """Loading API v1.0 executions...
        :param command: the command to be launched.
        :param query: the user name to be searched.

        This application can received a random number set by the administrator
        that may allow the one who performs the query to run code. Use it with
        caution.
    """
    # Splitting the query
    splittedQuery = shlex.split(query)

    # Get info froo OSRFramework configuration files
    if SECRET_TOKEN and SECRET_TOKEN == request.args.get('secret_token'):
        params =  splittedQuery
    else:
        params = [splittedQuery[0]]

    # Selecting the appropriate program
    if  command == "domainfy":
        args = domainfy.getParser().parse_args(['-n'] + params)
        answer = domainfy.main(args)
    elif  command == "entify":
        args = entify.getParser().parse_args(['-w'] + params)
        answer = entify.main(args)
    elif command == "mailfy":
        args = mailfy.getParser().parse_args(['-n'] + params)
        answer = mailfy.main(args)
    elif command == "phonefy":
        args = phonefy.getParser().parse_args(['-n'] + params)
        answer = phonefy.main(args)
    elif command == "searchfy":
        args = searchfy.getParser().parse_args(['-q'] + params)
        answer = searchfy.main(args)
    elif command == "usufy":
        args = usufy.getParser().parse_args(['-n'] + params)
        answer = usufy.main(args)
    # Grabbing current Time
    osrfTimestamp, osrfDate = _getServerTime()

    if answer != None:
        return flask.Response(
            json.dumps({
                    "code": 200,
                    "content": answer,
                    'date': osrfDate,
                    "description": "200 OK. The response contains an entity corresponding to the requested resource.",
                    'timestamp': osrfTimestamp
                },
                indent=2,
                sort_keys=True
            ),
            status=200,
            mimetype="application/json"
        )
    else:
        abort(400)


def _getServerTime():
    """Get current time and date.
    """
    t = time.time()
    d = time.ctime(int(time.time()))
    return t, d


# ----------------
# Error Management
# ----------------


@app.errorhandler(400)
def general_error(error):
    """400 Bad Request. The server cannot or will not process the request due to an apparent client error (e.g., malformed request syntax, too large size, invalid request message framing, or deceptive request routing).
    """
    return render_template(
        'error.html',
        errorCode='400',
        errorDescription="Client Error: 400 Bad Request. The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)."
    ), 400


@app.errorhandler(403)
def not_found_error(error):
    """403 Forbidden. The request was a valid request, but the server is refusing to respond to it. The user might be logged in but does not have the necessary permissions for the resource.
    """
    return render_template(
        'error.html',
        errorCode='403',
        errorDescription='Client Error: 403 Forbidden. The request was a valid request, but the server is refusing to respond to it.'
    ), 403


@app.errorhandler(404)
def not_found_error(error):
    """404 Not Found. Thee requested resource could not be found but may be available in the future. Subsequent requests by the client are permissible.
    """
    return render_template(
        'error.html',
        errorCode='404',
        errorDescription='Client Error: 404 Not Found. The requested resource could not be found but may be available again in the future. Subsequent requests by the client are permissible.',
    ), 404


# --------------
# Launching code
# --------------


if __name__ == "__main__":
    DEFAULT_VALUES = configuration.returnListOfConfigurationValues("osrframework-server")

    try:
        SECRET_TOKEN = DEFAULT_VALUES["secret_token"]
    except:
        SECRET_TOKEN = None

    # Loading the server parser
    parser = argparse.ArgumentParser(
        description='OSRFramework Server - The tool that will start a local server.',
        prog='./osrframework-server.py',
        epilog="Check the README.md file for further details on the usage of this program or follow us on Twitter in <http://twitter.com/i3visio>.",
        add_help=False
    )

    # adding the option
    groupServerConfiguration = parser.add_argument_group('Configuration arguments', 'Configuring the processing parameters.')
    groupServerConfiguration.add_argument('--host', metavar='<IP>', required=False, default=DEFAULT_VALUES["host"], action='store', help='choose the host in which the server will be accesible. If "0.0.0.0" is choosen, the server will be accesible by any remote machine. Use this carefully. Default: localhost.')
    groupServerConfiguration.add_argument('--port', metavar='<PORT>', required=False, default=DEFAULT_VALUES["port"], type=int, action='store', help='choose the port in which the server will be accesible. Use this carefully.')
    groupServerConfiguration.add_argument('--debug', required=False, default=DEFAULT_VALUES["debug"], action='store_true', help='choose whether error messages will be deployed. Do NOT use this for production.')

    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    groupAbout.add_argument('--version', action='version', version='%(prog)s ' + " " + osrframework.__version__, help='shows the version of the program and exists.')

    # Parse args
    args = parser.parse_args()

    app.run(
        debug=args.debug,
        host=args.host,
        port=args.port
    )