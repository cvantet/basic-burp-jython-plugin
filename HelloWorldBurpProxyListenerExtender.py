'''
Created on Feb 25, 2017

IProxyListener is used to parse and automatically modify your request/response
displayed in the Proxy tab when you intercept the traffic.

Below example adds a new cookie Helloworld and capitalize the request body.

@author: cvantet
'''
from burp import IBurpExtender, IProxyListener

import sys, os


def update_jython_path(burp_extension_path=('jython_libs','hello_world')):
    """
    To use any external Python package, you can use this function to update your
    path without installing any package in Python\Libs
    """
    current_path = os.path.join(os.getcwd())
    for i in burp_extension_path: current_path = os.path.join(current_path, i)
    sys.path.append(current_path)

update_jython_path()

from utils import jython_exception_catcher

def modify_header(header):
    header.add("Cookie: Helloworld:test;")
    return header

def modify_body(body):
    return body.upper() if body else ""

def display_debug(headers, body, sheaders, msg):
    separator = "#"*10
    print "#REQUEST#" 
    print '%s' % '\n'.join(headers)
    print body
    print separator
    print "#EDITED REQUEST#"
    print '%s' % '\n'.join(sheaders)
    print msg
    print separator
    
    

@jython_exception_catcher
def do_simple_process(http_extender, messageIsRequest, request):
    if not messageIsRequest:
        print 'Message is a response.'
        return
    content = request.getRequest()
    parsed_request = http_extender.helpers.analyzeRequest(content)
    header = parsed_request.getHeaders()
    body = content[parsed_request.getBodyOffset():].tostring()
    
    #Modify those methods to parse/analyze/do what you want to do
    sheader = modify_header(header)    
    msg = modify_body(body)
    display_debug(header, body, sheader, msg)
    
    #creating the edited request
    if msg: sbody = http_extender.helpers.bytesToString(msg)
    else: sbody = http_extender.helpers.bytesToString(body)
     
    request.setRequest(http_extender.helpers.buildHttpMessage(sheader, sbody))
  

class BurpExtender(IBurpExtender, IProxyListener):
    
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName('HelloWorldBurpTabExtender')
        self.callbacks.registerProxyListener(self)
        
    def processProxyMessage(self, messageIsRequest, message):
        do_simple_process(self, messageIsRequest, message.getMessageInfo())