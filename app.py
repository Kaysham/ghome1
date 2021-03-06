# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import http.client

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Requestasse:")
    # print(json.dumps(req, indent=4))

    res = processRequest2(req)

    res = json.dumps(res, indent=4)
    # print("retour res=",res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest2(req):
    if req.get("result").get("action") != "Djamboui":
       return {}

    # print("Responseasse:")
    result     = req.get("result")
    parameters = result.get("parameters")
    p_action   = parameters.get("p_action")
    p_objet    = parameters.get("p_objet")

    connection = http.client.HTTPConnection('testsced.kalanda.info')
    headers = {'Content-type': 'application/json'}

    #foo = {"Action":"allumer","Objet":"lampe"}
    foo = {}
    foo["Action"] = p_action
    foo["Objet"]  = p_objet
    
    json_foo = json.dumps(foo)
 
    url_webservice = "/Safire/Commande"
    connection.request('POST', url_webservice, json_foo, headers=headers)
    response = connection.getresponse()

    data = response.read().decode()
    print(data)
    
    donnees     = json.loads(data)
    speech      = donnees["speech"]
    displayText = donnees["displayText"]
    source      = donnees["source"]
   
    return {
      "speech": speech,
      "displayText": displayText,
      # "data": data,
      # "contextOut": [],
      "source": source

    }
      
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
