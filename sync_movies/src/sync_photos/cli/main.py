import argparse
import sys
import os
import time
import re
import exifread

# def get_file_year_month(folder: str, name: str):
#    created = os.path.getctime(os.path.join(folder, name))
#    year, month, _, _, _, _ = time.localtime(created)[:-3]
#    print("%s %d %d " %( os.path.join(folder, name), year, month))
#    sys.exit(1)
#    return (str(year), str(month))

batch_file_name = "batch_photos.sh"

def get_file_year_month(folder: str, name: str):
    filename = os.path.join(folder, name)
    with open(filename, 'rb') as fh:
        print("%40s is analyzing ...\r" % filename)
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        if ("EXIF DateTimeOriginal" not in tags):
            raise KeyError("DateTimeOriginal does not exist")
        date_taken = tags["EXIF DateTimeOriginal"]
        p = re.compile(r'^(\d{4}):(\d{2}):(\d{2})\s+(\d{2}):(\d{2}):(\d{2})$')
        m = p.match(str(date_taken))
        if (m):
            (year, month, _, _, _, _) = (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
        else:
            raise ValueError("Invalid date format %s" % date_taken)
    return (year, month)


def sync_path(src_folder: str, dest_folder: str):
    files_list = []
    path_list = set()
    for root, _, files in os.walk(src_folder):
        for name in files:
            p = re.compile(r'(?:[\w\-\s]+)\.(jpg)$', re.IGNORECASE)
            m = p.match(name)
            if (m):
                try:
                    #print(os.path.join(root, name))
                    (year, month) = get_file_year_month(root, name)
                    date_path = os.path.join(year, month)
                    path_list.add(date_path)
                    files_list.append({'path': root, 'date_path': date_path, 'format': m.group(1), 'year': year, 'month': month, 'name': name})
                except Exception as err:
                    print("%s is skipped due to %s" % (name, err))
                

    # with open(os.path.join(src_folder, 'batch_movies.sh'), 'w') as writer:
    print("Write to %s" % batch_file_name)
    with open(batch_file_name, 'w') as writer:
        for path_name in sorted(path_list):
            if not os.path.exists(os.path.join(dest_folder, path_name)):
                writer.write('mkdir -p "%s" \n' % os.path.join(dest_folder, path_name))
        writer.write("\n")

        for file_info in files_list:
            if os.path.exists(os.path.join(dest_folder, file_info['name'])):
                writer.write("# skip %s" % (os.path.join(
                    file_info['path'], file_info['name'])))
            else:
                writer.write('echo "Moving %s ..."\n' % (
                    os.path.join(file_info['path'], file_info['name'])))
                writer.write('mv "%s" "%s"\n' % (os.path.join(file_info['path'], file_info['name']),
                                                 os.path.join(dest_folder, file_info['date_path'])))
                # os.system('mv "%s" "%s"\n' % (os.path.join(file_info['path'], file_info['name']),
                #    os.path.join(dest_folder, file_info['year'])))

    os.chmod(batch_file_name, 0o755)


def sync_photos_cli():
    parser = argparse.ArgumentParser(description="Synchronize the photos")
    parser.add_argument("source", help="specify source folder of photos")
    parser.add_argument("destination", help="specify destination folder of photos")
    args = parser.parse_args()
    if (args.source == None or args.destination == None):
        parser.print_help()
        sys.exit(1)

    try:
        sync_path(args.source, args.destination)
    except Exception as err:
        print(err)
