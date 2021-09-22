from os import walk, mkdir

from docx2pdf import convert

path = "D:/UserData/Google Drive/NCKUH/實驗室安全/工作區/防災演習/檢點表/"
export_folder_name = "export"

try:
    mkdir(path + export_folder_name)
except FileExistsError:
    pass


def get_files(path):
    docx_files = []
    for fs in walk(path):
        for f in fs[2]:
            fname, fext = f.split(".")
            if fext == "docx":
                docx_files.append((path + f, path + "export/" + fname + ".pdf"))
    return docx_files


def convert2pdf(files_list):
    for f in files_list:
        convert(f[0], f[1])


if __name__ == "__main__":
    files = get_files(path)
    convert2pdf(files)

