from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

myWV = QWebView(None)
myWV.load(QUrl('https://wikipedia.org/wiki/[%Name%]'))
myWV.show()