from Utils.KMS import DocServer


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
        self._soup = soup
        self.files = {}

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
