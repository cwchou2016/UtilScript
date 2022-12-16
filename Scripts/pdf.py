from os import walk, mkdir, path

from docx2pdf import convert


def get_files(f_path):
    docx_files = []
    for fs in walk(f_path):
        for f in fs[2]:
            fname, fext = path.splitext(f)
            if fext == ".docx":
                docx_files.append((f"{f_path}{f}", f"{f_path}export/{fname}.pdf"))

    return docx_files


def convert2pdf(files_list):
    for f in files_list:
        convert(f[0], f[1])


if __name__ == "__main__":
    f_path = "G:/我的雲端硬碟/工作區/118/附件/"
    export_folder_name = "export"

    try:
        mkdir(f_path + export_folder_name)
    except FileExistsError:
        pass

    files = get_files(f_path)

    print(files)
    for f in files:
        print(f[0])
    convert2pdf(files)
