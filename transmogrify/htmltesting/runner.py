from collective.transmogrifier.tests import registerConfig
from collective.transmogrifier.transmogrifier import Transmogrifier
from pkg_resources import resource_string, resource_filename
from collective.transmogrifier.transmogrifier import configuration_registry
from Products.Five import zcml
from zope.component import provideUtility
from zope.interface import classProvides, implements
import transmogrify.htmltesting
import re

class Context:
    pass


CONFIG = """

[clean]
blueprint = collective.transmogrifier.sections.manipulator
delete = 
    %(strip)s

[printer]
blueprint = collective.transmogrifier.sections.tests.pprinter

"""


 
def runner(config, args={}):
    from collective.transmogrifier.transmogrifier import Transmogrifier
#    test.globs['transmogrifier'] = Transmogrifier(test.globs['plone'])

    import zope.component
    import zope.app.component
    import collective.transmogrifier.sections
    zcml.load_config('meta.zcml', zope.app.component)
    zcml.load_config('meta.zcml', collective.transmogrifier)
    zcml.load_config('configure.zcml', collective.transmogrifier.sections)
    zcml.load_config('configure.zcml', transmogrify.htmltesting)


    context = Context()
    configuration_registry.registerConfiguration(
        u'transmogrify.config.funnelweb',
        u"",
        u'', config)

    transmogrifier = Transmogrifier(context)
    overrides = {}
    if type(args) == type(''):
      for arg in args:
        section,keyvalue = arg.split(':',1)
        key,value = keyvalue.split('=',1)
        overrides.setdefault('section',{})[key] = value
    else:
        overrides = args

    transmogrifier(u'transmogrify.config.funnelweb', **overrides)




def testtransmogrifier(config, strip=['_content']):
    strip = '\t'+'\n\t'.join(strip)

    config = re.sub('\.\.\.',config, 'clean\n\tprinter\n')
    config += CONFIG
    config = config % locals()
    
    runner(config)

if __name__ == '__main__':
       main()
