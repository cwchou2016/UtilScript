class Document:
    def __init__(self, doc_id, soup):
        """
        :param doc_id:
        :param soup: BeautifulSoup of document page.
        """
        self._doc_id = doc_id
        self._soup = soup
        self.files = {}
        self.load_files()

    def load_files(self):
        """
        Get files download link.
        """
        files = self._soup.find_all("div", {"class": "documentmode-file-title"})

        for f in files:
            size_text = f.find("span")
            size_text.extract()

            f_name = f.get_text.strip()
            link = self._soup.find("a", {"title": f_name + " "})

            self.files[f_name] = link

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
        pass
