import argparse
import sys
import os
import re
from PyPDF2 import PdfFileReader
import isbnlib
import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup


def get_book_info(root: str, name: str):
    pdf_reader = PdfFileReader(os.path.join(root, name))
    print(pdf_reader.getDocumentInfo())


def convert_to_asin(isbn: str) -> str:
    if (isbnlib.is_isbn13(isbn)):
        asin = isbnlib.to_isbn10(isbn)
    elif (isbnlib.is_isbn10(isbn)):
        asin = isbn
    else:
        raise ValueError("Invalid ISBN %s" % isbn)
    return asin


def get_book_info_by_asin(asin: str):
    headers = {'user-agent': 'Mozilla/5.0'}  # Mozilla/5.0是浏览器很标准的字段
    cookie_jar = RequestsCookieJar()
    cookie_jar.set("session-id", "138-7481364-9854305", domain="amazon.com")
    url = "https://www.amazon.com/dp/%s" % asin
    print("Loading page %s" % url)
    r = requests.get(url, headers=headers, cookies=cookie_jar)
    if (r.status_code == 200):
        print("Loaded page %s" % url)
    #print(r.request.headers)
    #print(r.text)
    #print(r.cookies)
    #sys.exit(1)
    soup = BeautifulSoup(r.text, 'lxml')
    product_details = soup.select('ul[class="detail-bullet-list"] > span[class="a-list-item"] > span')
    for d in product_details:
        print(d)
    sys.exit(1)


def sync_path(src_folder: str, dest_folder: str):
    files_list = []
    path_list = set()
    for root, _, files in os.walk(src_folder):
        p = re.compile(r'(?:.*\/)?([\dX]+)(?:\s+epub)?', re.IGNORECASE)
        m = p.match(root)
        if (m):
            asin = convert_to_asin(m.group(1))
            get_book_info_by_asin(asin)
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
                    files_list.append(
                        {'path': root, 'year': m.group(1), 'name': name})

    # with open(os.path.join(src_folder, 'batch_movies.sh'), 'w') as writer:
    with open('batch_books.sh', 'w') as writer:
        for path_name in sorted(path_list):
            if not os.path.exists(os.path.join(dest_folder, path_name)):
                writer.write('mkdir -p "%s" \n' %
                             os.path.join(dest_folder, path_name))
        writer.write("\n")

        for file_info in files_list:
            if os.path.exists(os.path.join(dest_folder, file_info['name'])):
                writer.write("# skip %s" % (os.path.join(
                    file_info['path'], file_info['name'])))
            else:
                writer.write('echo "Moving %s ..."\n' % (
                    os.path.join(file_info['path'], file_info['name'])))
                writer.write('mv "%s" "%s"\n' % (os.path.join(file_info['path'], file_info['name']),
                                                 os.path.join(dest_folder, file_info['year'])))
                # os.system('mv "%s" "%s"\n' % (os.path.join(file_info['path'], file_info['name']),
                #    os.path.join(dest_folder, file_info['year'])))

    os.chmod('batch_movies.sh', 0o755)


def sync_books_cli():
    parser = argparse.ArgumentParser(description="Synchronize the books")
    parser.add_argument("source", help="specify source folder of book")
    parser.add_argument(
        "destination", help="specify destination folder of book")
    args = parser.parse_args()
    if (args.source == None or args.destination == None):
        parser.print_help()
        sys.exit(1)

    try:
        sync_path(args.source, args.destination)
    except Exception as err:
        print(err)
