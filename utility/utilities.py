import contextlib
import csv
import os

from config.properties import Properties


def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files():
    create_project_dir(Properties.folder)
    queue = Properties.queue_file
    crawled = Properties.crawled_file
    spelling = Properties.spelling_file
    broken_images = Properties.broken_images_file
    broken_links = Properties.broken_links_file
    blank_pages = Properties.blank_pages_file
    if not os.path.isfile(queue):
        write_file(queue, Properties.home_page + "," + str(0))
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(spelling):
        write_file(spelling, '')
    if not os.path.isfile(broken_links):
        write_file(broken_links, '')
    if not os.path.isfile(broken_images):
        write_file(broken_images, '')
    if not os.path.isfile(blank_pages):
        write_file(blank_pages, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    with open(file_name, 'rt') as f:
        results = [tuple(line) for line in csv.reader(f)]
    parsed = ((row[0],
               int(row[1])) for row in results)
    return set(parsed)


# Iterate through a set, each item will be a line in a file
def set_to_file(data, file_name):
    with open(file_name, "w") as out:
        csv_out = csv.writer(out)
        for row in sorted(data, key=lambda x: x[0]):
            with ignored(UnicodeEncodeError):
                csv_out.writerow(row)


@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass
