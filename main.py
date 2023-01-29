import argparse
import pathlib
import os
from pypdf import PdfWriter

parser = argparse.ArgumentParser(
    description="Command line utility to join PDFs")
parser.add_argument("folder", help="folder with all pdfs to be joined",
                    type=pathlib.Path, default=".", metavar="/path/to/pdf/folder")
parser.add_argument(
    "-f", "--force", help="delete file on output conflict", action="store_true")
args = parser.parse_args()
folder = args.folder

if (not folder.exists() or not folder.is_dir()):
    raise Exception("Invalid folder")

files = sorted(os.listdir(folder))


pdfs = [folder / file for file in files if os.path.isfile(
    str(folder)+"/"+file) and file.endswith(".pdf") and not file == "joined.pdf"]


output = folder / "joined.pdf"
if (output.exists()):
    if (args.force is True):
        output.unlink()
    else:
        raise Exception("File {0} already exists, add -f / --force to delete existing file".format(str(output)))

merger = PdfWriter()

for pdf in pdfs:
    merger.append(str(pdf))
merger.write(str(output))
merger.close()
print("Done, written joined pdf at {0}".format(str(output)))
