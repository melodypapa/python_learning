import argparse
import sys
import os
import re

def sync_path(src_folder: str, dest_folder: str):
    files_list = []
    path_list = set()
    for root, _, files in os.walk(src_folder):
        for name in files:
            p = re.compile(r'.*(\d{4})\.(?:[\w\-.]+)\.mkv$', re.IGNORECASE)
            m = p.match(name)
            if (m):
                path_list.add(m.group(1))
                files_list.append({'path': root, 'year': m.group(1), 'name': name})

    batch_name = 'batch_movies.sh'
    move_cmd = 'mv'
    #with open(os.path.join(src_folder, 'batch_movies.sh'), 'w') as writer:
    if (sys.platform == "win32"):
        batch_name = 'batch_movies.bat'
        move_cmd = 'move' 
    with open(batch_name, 'w', encoding='utf-8') as writer:
        for path_name in sorted(path_list):
            if not os.path.exists(os.path.join(dest_folder, path_name)):
                writer.write('mkdir -p "%s" \n' % os.path.join(dest_folder, path_name))
        writer.write("\n")

        for file_info in files_list:
            if os.path.exists(os.path.join(dest_folder, file_info['year'], file_info['name'])):
                writer.write("# skip %s\n" % (os.path.join(file_info['path'], file_info['name'])))
            else:
                writer.write('echo "Moving %s ..."\n' % (os.path.join(file_info['path'], file_info['name'])))
                writer.write('%s "%s" "%s"\n' % (move_cmd, os.path.join(file_info['path'], file_info['name']), 
                    os.path.join(dest_folder, file_info['year'])))
                #os.system('mv "%s" "%s"\n' % (os.path.join(file_info['path'], file_info['name']), 
                #    os.path.join(dest_folder, file_info['year'])))
    if (sys.platform != "win32"):
        os.chmod('batch_movies.sh', 0o755)

def sync_movies_cli():
    parser = argparse.ArgumentParser(description="Synchronize the movies")
    parser.add_argument("source", help="specify source folder of movies")
    parser.add_argument("destination", help="specify destination folder of movies")
    args = parser.parse_args()
    if (args.source == None or args.destination == None):
        parser.print_help()
        sys.exit(1)

    try:
        sync_path(args.source, args.destination)
    except Exception as err:
        #print(err)
        raise(err)
    