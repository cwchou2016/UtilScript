import json
import re

from Utils.KMS import DocServer
from Utils.KMS.DocException import CreateDocException


class Document:
    """
    Load document information from BeatuifulSoup web page.

    """

    def __init__(self, soup):
        """
        :param soup: BeautifulSoup of document page.
        """
        self._doc_id = None
        self._version = None
        self._doc_name = None
        self._soup = soup
        self.files = {}

        self.read_doc_name()
        self.read_files()
        self.read_doc_id()
        self.read_version()

    def read_files(self):
        """
        Read files of the document
        """
        files = self._soup.find_all("div", {"class": "documentmode-file-title"})

        for f in files:
            size_text = f.find("span")
            size_text.extract()

            f_name = f.get_text().strip()
            link = self._soup.find("a", {"title": f_name + " "})

            if link is None:
                self.files[f_name] = None
            else:
                self.files[f_name] = DocServer.HOST + link.get("href")

    def read_doc_name(self):
        """
        Read the document name
        """
        tag = self._soup.find("h3", {"class": "title_zh-TW"})

        if tag:
            self._doc_name = tag.get_text().strip()

    def read_doc_id(self):
        """
        Read document's id
        """
        id_tag = self._soup.find("form", {"name": "aspnetForm"})

        if id_tag is not None:
            doc_id = id_tag.get("action").split("=")[1]
            self._doc_id = doc_id

    def read_version(self):
        """
        Read the latest version number
        """
        ver = self._soup.find("span", {"id": "ctl00_cp_latestVersion"})

        if ver is None:
            self._version = 1
            return

        self._version = ver.get_text()

    def get_files_link(self):
        """
        Get all download links of files if download is available.
        :return: dictionary of files with its download links.
        """
        return self.files

    def get_view_link(self):
        """
        Generate the links of the preview window.
        :return: dictionary of files with its view links.
        """
        view_links = {}
        for f in self.files:
            view_links[f] = DocServer.DocServer.doc_view_link + \
                            f"?documentid={self.get_id()}&ver={self.get_version()}&filename={f}&type=file"
        return view_links

    def get_id(self):
        return self._doc_id

    def get_version(self):
        return self._version

    def __str__(self):
        return f"Document Name:{self._doc_name}\n" \
                f"Document ID: {self.get_id()} \n" \
                f"Version: {self.get_version()} \n" \
                f"File Name: {self.get_files_link()}"


class Draft:
    """Load draft from beatuifulsoup of create document page."""
    def __init__(self, soup):
        self._soup = soup

        # payload value
        self._d = self.get_draft_object() #draftObject
        self._r = [] #relation files
        self._p = self.get_folder_id() #folder
        self._propagation= 1
        self._gid = None
        self._dti = None
        self._rs = self.get_random_suffix()
        self._dd = "99991231235959"
        self._ad = "17530101000000"
        self._usenewdocclass = "false"
        self._isnewdraft = "false"

        self.parse_draft()

    def parse_draft(self):
        """parse draft object"""
        pass

    def get_draft_object(self) -> dict:
        """
        get draft object

        return: draft object
        """
        tag = self._soup.find('script', string=re.compile('var draftObj'))

        if tag:
            pattern = r'var draftObject\s*=\s*(\{.*?\});'
            match = re.search(pattern, tag.string, re.DOTALL)

            if match:
                json_str = match.group(1)
                return json.loads(json_str)

        raise CreateDocException("Draft object not found.")

    def get_folder_id(self) -> str:
        """
        get folder id

        return folder id
        """
        tag = self._soup.find('script', string=re.compile('var folderId'))

        if tag:
            pattern = r'var folderId = "(\d+)";'
            match = re.search(pattern, tag.string, re.DOTALL)

            if match:
                json_str = match.group(1)
                return str(json.loads(json_str))

        raise CreateDocException("Folder ID not found.")

    def get_random_suffix(self) -> str:
        """
        return random suffix
        """
        rs = self._soup.find('input', {'name': 'ctl00$cp$RandomSuffix'}).get('value')
        if rs:
            return rs

        raise CreateDocException("Random suffix not found.")

    def get_payload(self):
        """get payload"""
        payload = {
            "gid":self._gid,
            "rs":self._rs,
            "p": self._p,
            "d": self._d, # TODO: change to text format
            "r": self._r,
            "ad": self._ad,
            "dd": self._dd,
            "dti": self._dti,
            "usenewdocclass": self._usenewdocclass,
            "isnewdraft": self._isnewdraft,
        }

        return payload

    def set_title(self, title):
        """set draft title"""
        pass

    def get_title(self):
        """get document title"""
        pass

    def get_draft_id(self):
        """get draft id"""

    def get_draft_obj(self):
        """get draft object"""
        pass