from Utils.KMS import DocServer


class Document:
    def __init__(self, soup):
        """
        :param doc_id:
        :param soup: BeautifulSoup of document page.
        """
        self._doc_id = None
        self._soup = soup
        self.files = {}
        self.load_doc()

    def load_doc(self):
        """
        Get document info.
        """

        id_tag = self._soup.find("form", {"name": "aspnetForm"})
        doc_id = id_tag.get("action").split("=")[1]

        self._doc_id = doc_id

        files = self._soup.find_all("div", {"class": "documentmode-file-title"})

        for f in files:
            size_text = f.find("span")
            size_text.extract()

            f_name = f.get_text().strip()
            link = self._soup.find("a", {"title": f_name + " "})

            if link is None:
                self.files[f_name] = None
            else:
                self.files[f_name] = link.get("href")

    def get_latest_version(self):
        """
        :return: The latest version number from the document page
        """
        ver = self._soup.find("span", {"id": "ctl00_cp_latestVersion"})

        if ver is None:
            return 1

        return ver

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
                            f"?documentid={self.get_id()}&ver={self.get_latest_version()}&filename={f}&type=file"
        return view_links

    def get_id(self):
        return self._doc_id
