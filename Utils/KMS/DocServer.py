import getpass
import os
import shutil

import requests
from bs4 import BeautifulSoup

from .Document import Document

HOST = "http://kms.hosp.ncku.edu.tw/KM/"

CODE = {0: "Success", 404: "Failed"}


class DocServer:
    login_link = HOST + "login.aspx"
    logout_link = HOST + "logout.aspx"
    doc_link = HOST + "readdocument.aspx"
    doc_view_link = HOST + "preview.aspx"

    def __init__(self):
        self._user_data = {}
        self._session = requests.session()
        self._response = self._session.get(DocServer.login_link)

        soup = self.get_soup()
        self._user_data["__VIEWSTATE"] = soup.find('input', {'id': "__VIEWSTATE"}).get("value")
        self._user_data["__VIEWSTATEGENERATOR"] = soup.find('input', {'id': "__VIEWSTATEGENERATOR"}).get("value")
        self._user_data["__EVENTVALIDATION"] = soup.find('input', {'id': "__EVENTVALIDATION"}).get("value")
        self._user_data['LoginButton'] = soup.find('input', {'id': "LoginButton"}).get("value")
        self._user_data["txtOpenIdUser"] = ""

    def get_soup(self):
        return BeautifulSoup(self._response.content, "html.parser")

    def login(self, user, password):
        """
        :return: int CODE
        """
        self._user_data['txtUserName'] = user
        self._user_data['txtPassword'] = password

        self._response = self._session.post(DocServer.login_link, data=self._user_data)
        soup = self.get_soup()

        if soup.find("a", {"href": "/KM/logout.aspx"}) is None:
            return 404

        return 0

    def logout(self):
        self._response = self._session.get(DocServer.logout_link)
        soup = self.get_soup()

        if soup.find("a", {"href": "/KM/logout.aspx"}) is None:
            return 404

        return 0

    def read_doc_by_id(self, doc_id):
        """
        Get document information
        :param doc_id:
        :return: Document
        """
        link = DocServer.doc_link + f"?documentId={doc_id}"
        self._response = self._session.get(link)

        soup = self.get_soup()
        if soup.find("div", {"class": "errorMessage"}) is not None:
            return None  # TODO raise Exception here

        doc = Document(soup)
        return doc

    def download_view_url(self, url):
        """
        Download pdf from online pdf viewer
        """
        self._response = self._session.get(url)
        soup = self.get_soup()

        links = soup.find_all("a", {"class": "page-data-link"})
        title = (str(soup.title.string).strip()).split(".")[0]

        print(os.getcwd(), title)

        try:
            os.makedirs(f"export/{title}/")
        except FileExistsError:
            shutil.rmtree(f"export/{title}/")
            os.makedirs(f"export/{title}/")

        page_number = 1
        for i in links:
            img_link = HOST + i.get("href")

            content = self._session.get(img_link).content

            with open(f"export/{title}/{page_number:03}.jpg", "wb") as f:
                f.write(content)
                page_number += 1

    def download_file_url(self, f_name, url):
        """
        Download file
        :param f_name: file name
        :param url:  file link
        """
        content = self._session.get(url).content
        with open(f"export/{f_name}", "wb") as f:
            f.write(content)


if __name__ == "__main__":

    user = input("User:")
    password = getpass.getpass()

    server = DocServer()
    result = server.login(user, password)

    if result != 0:
        print("Login not success!")

    # with open("download_urls.txt", "r") as f:
    #     for url in f.readlines():
    #         server.download_view_url(url)
