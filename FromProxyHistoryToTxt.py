'''
Created on Nov 1, 2017

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


@jython_exception_catcher
def create_file(http_extender):
    history = http_extender.callbacks.getProxyHistory()
    f = open('proxy_history.txt', 'w+')
    i = 0
    for element in history:
        process_proxy_element(http_extender, element, f, i)
        i+=1
    f.close()

def process_proxy_element(http_extender, element, f, i):
    f.write('#### REQUEST %d ####\n' % i)
    content = element.getRequest()
    parsed_request = http_extender.helpers.analyzeRequest(content)
    headers = parsed_request.getHeaders()
    body = content[parsed_request.getBodyOffset():].tostring()
    f.write('%s\n' % '\n'.join(headers))
    f.write('%s\n' % body)
    f.write('\n#### RESPONSE %d ####\n' % i)
    content = element.getResponse()
    parsed_request = http_extender.helpers.analyzeResponse(content)
    headers = parsed_request.getHeaders()
    body = content[parsed_request.getBodyOffset():].tostring()
    f.write('%s\n' % '\n'.join(headers))
    f.write('%s\n' % body)


    
class BurpExtender(IBurpExtender):
    
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName('FromProxyHistoryToTxt')
        create_file(self)
        
