from bs4 import BeautifulSoup
import requests
import re
from PySide2 import QtCore


_BASE_URL = "https://www.tukui.org"
_ELV_UI_DOWNLOAD_PAGE = "https://www.tukui.org/download.php?ui=elvui"
_DOWNLOAD_BUTTON_CLASS = "btn btn-mod btn-border-w btn-round btn-large"
_HREF_REGEX = r"/downloads/elvui-(?P<version>\d+\.\d+)\.zip"


class Downloader(QtCore.QObject):

    download_finished = QtCore.Signal()

    def __init__(self, parent=None):
        super(Downloader, self).__init__(parent=parent)
        self._page = requests.get(_ELV_UI_DOWNLOAD_PAGE)
        if self.is_webpage_down():
            raise ValueError(
                "I cannot connect to '{}'.Is it down?".format(_ELV_UI_DOWNLOAD_PAGE)
            )

    def is_webpage_down(self):
        if self._page.status_code != 200:
            return True
        return False

    def get_download_button(self):
        soup = BeautifulSoup(self._page.content, "html.parser")
        download_button = soup.find("a", href=re.compile(_HREF_REGEX))
        return download_button

    def is_download_button_available(self):
        download_button = self.get_download_button()
        if not download_button:
            return False
        return True

    def get_version(self):
        download_button = self.get_download_button()
        match = re.match(_HREF_REGEX, download_button.attrs.get("href"))
        if not match:
            raise ValueError(
                "Cannot retrieve the 'Version' field. Please contact the Developer"
            )
        return match.groupdict().get("version")

    def download(self):
        if not self.is_download_button_available():
            raise ValueError("Download link not accessible. Contact the Developer")
        download_button = self.get_download_button()
        full_link = "{}{}".format(_BASE_URL, download_button.attrs.get("href"))
        downloaded_file = requests.get(full_link)
        self.download_finished.emit()
        return downloaded_file


if __name__ == "__main__":
    downloader = Downloader()
    print(downloader.download())
#
# z = zipfile.ZipFile(io.BytesIO(r.content))
# z.extractall(r"C:\Program Files (x86)\World of Warcraft\_retail_\Interface\AddOns")
