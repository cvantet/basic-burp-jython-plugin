'''
Created on Feb 24, 2017
Below example is to simply add a new Message editor and display "Helloworld"
in the request field.

@author: cvantet
'''
from burp import IBurpExtender, IMessageEditorTab, IMessageEditorTabFactory

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


class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName('HelloWorldBurpTabExtender')
        self.callbacks.registerMessageEditorTabFactory(self)
        

    def createNewInstance(self, controller, editable):
        """
        Method which needs to be overrided to implement IMessageEDitorTabFactory
        https://portswigger.net/burp/extender/api/burp/IMessageEditorTabFactory.html  
        """
        return HelloWorldBurpTab(self, controller, editable)

class HelloWorldBurpTab(IMessageEditorTab):
    
    def __init__(self, extender, controller, editable):
        self.extender = extender
        self.controller = controller
        self.editable = editable
        self.helpers = self.extender.helpers
        self.editor = self.extender.callbacks.createTextEditor()
        self.editor.setEditable(editable)
        
    
    def getTabCaption(self):
        return "HelloWorldBurpTab"
    
    def getUiComponent(self):
        return self.editor.getComponent()
    
    def isEnabled(self, content, isRequest):
        return isRequest
    
    def setMessage(self, content, isRequest):
        if isRequest:
            self.editor.setText('HelloWorld')
