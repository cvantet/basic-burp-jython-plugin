'''
Created on Feb 24, 2017

@author: cvantet
'''
import traceback

class jython_exception_catcher():
    """
    Annotation to catch any Jython exception raised from any of your Python package.
    Unfortunately, this does not work for any Jython class.
    """
    def __init__(self, function):
        print function
        self.function = function
    def __call__(self, *args):
        print 'Executing %s with arguments[%s]...' % (self.function.__name__,\
                                                      ','.join(["(%s):%s" % (type(arg), str(arg)) for arg in args]))
        try:
            self.function(*args)
        except:
            tb = traceback.format_exc()
            print tb
        

def identify_http_message_source(tool_flag):
    flags = {
        1:'Suite',
        2:'Target',
        4:'Proxy',
        8:'Spider',
        16:'Scanner',
        32:'Intruder',
        64:'Repeater',
        128:'Sequencer',
        256:'Decoder',
        512:'Comparer',
        }
    flag_name = flags[tool_flag] if tool_flag in flags.keys() else 'Unknwon flag %d' % tool_flag
    print flag_name
    return flag_name
        