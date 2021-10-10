from os import walk, mkdir

from docx2pdf import convert


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
    from tkinter import Tk, filedialog

    tk = Tk()
    tk.withdraw()
    path = filedialog.askdirectory() + "/"

    print(path)
 
    export_folder_name = "export"

    try:
        mkdir(path + export_folder_name)
    except FileExistsError:
        pass

    files = get_files(path)
    for f in files:
        print(f[0])
    convert2pdf(files)
