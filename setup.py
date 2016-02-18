from distutils.core import setup
import py2exe

DATA=[
    ('imageformats',[
        'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qjpeg4.dll',
        'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qgif4.dll',
        'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qico4.dll',
        'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qmng4.dll',
        'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qsvg4.dll',
        'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qtiff4.dll']),
    ('', ['main_window.ui'])]

setup(
    windows=['main.py'],
    options={'py2exe':{
        'includes': ['sip'],
        'excludes': ['PyQt4.uic.port_v3'],
        'packages': ['sqlalchemy.dialects.sqlite']}},
    data_files = DATA)