class Document:
    def __init__(self, doc_id, soup):
        self._doc_id = doc_id
        self._soup = soup
        self.files = {}

    def get_files(self):
        files = self._soup.find_all("div", {"class": "documentmode-file-title"})

        for f in files:
            size_text = f.find("span")
            size_text.extract()

            self.files[f.get_text().strip()] = ""

    def get_latest_version(self):
        pass

    def download_files(self):
        pass

    def downloadable(self):
        pass

    def viewable(self):
        pass

    def download_files(self):
        pass
