from getpass import getpass

from Utils.KMS.DocServer import DocServer

user = input("user:")
pw = getpass.getpass()

doc_id = input("document id:")

ds = DocServer()
ds.login(user, pw)

doc = ds.read_doc_by_id(doc_id)

view_links = doc.get_view_link()
file_links = doc.get_files_link()

for file in file_links:
    if file_links[file_links] is None:
        ds.download_view_url(view_links[file])
        continue

    ds.download_file_url(file, file_links[file])
