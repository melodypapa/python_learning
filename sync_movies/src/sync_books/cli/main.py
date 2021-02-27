import argparse
import sys, os, re
from PyPDF2 import PdfFileReader;
import isbnlib

def get_book_info(root:str, name: str):
    pdf_reader = PdfFileReader(os.path.join(root, name))
    print(pdf_reader.getDocumentInfo())

def sync_path(src_folder: str, dest_folder: str):
    files_list = []
    path_list = set()
    for root, _, files in os.walk(src_folder):
        p = re.compile(r'(?:.*\/)?([\dX]+)(?:\s+epub)?', re.IGNORECASE)
        m = p.match(root)
        if (m):
            files_list.append({'path': root, 'year': "", 'name': ""})
        else:
            for name in files:
                p = re.compile(r'([\dX]+)\.:json$', re.IGNORECASE)
                m = p.match(name)
                if (m):
                    print("Root  %s, name %s" % (root, name))
                    sys.exit(1)
                    get_book_info(root, name)
                    path_list.add(m.group(1))
                    files_list.append({'path': root, 'year': m.group(1), 'name': name})

    #with open(os.path.join(src_folder, 'batch_movies.sh'), 'w') as writer:
    with open('batch_books.sh', 'w') as writer:
        for path_name in sorted(path_list):
            if not os.path.exists(os.path.join(dest_folder, path_name)):
                writer.write('mkdir -p "%s" \n' % os.path.join(dest_folder, path_name))
        writer.write("\n")

        for file_info in files_list:
            if os.path.exists(os.path.join(dest_folder, file_info['name'])):
                writer.write("# skip %s" % (os.path.join(file_info['path'], file_info['name'])))
            else:
                writer.write('echo "Moving %s ..."\n' % (os.path.join(file_info['path'], file_info['name'])))
                writer.write('mv "%s" "%s"\n' % (os.path.join(file_info['path'], file_info['name']), 
                    os.path.join(dest_folder, file_info['year'])))
                #os.system('mv "%s" "%s"\n' % (os.path.join(file_info['path'], file_info['name']), 
                #    os.path.join(dest_folder, file_info['year'])))
    
    os.chmod('batch_movies.sh', 0o755)

def sync_books_cli():
    parser = argparse.ArgumentParser(description="Synchronize the books")
    parser.add_argument("source", help="specify source folder of book")
    parser.add_argument("destination", help="specify destination folder of book")
    args = parser.parse_args()
    if (args.source == None or args.destination == None):
        parser.print_help()
        sys.exit(1)

    try:
        sync_path(args.source, args.destination)
    except Exception as err:
        print(err)
    