import requests
import zipfile
import io
from PySide2 import QtCore


class Extractor(QtCore.QObject):
    def __init__(self, request: requests.models.Response, parent=None):
        super(Extractor, self).__init__(parent=parent)
        self._request = request

    def extract(self, path: str):
        zip = zipfile.ZipFile(io.BytesIO(self._request.content))
        zip.extractall(path)
