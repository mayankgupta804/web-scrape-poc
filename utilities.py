import os
import csv
import contextlib

from propertieshelper import PropertiesHelper


def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(config):
    p = PropertiesHelper(config)
    create_project_dir(p.folder)
    queue = p.queue_file
    crawled = p.crawled_file
    spelling = p.spelling_file
    broken_images = p.broken_images_file
    broken_links = p.broken_links_file
    if not os.path.isfile(queue):
        write_file(queue, p.home_page + "," + str(0))
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(spelling):
        write_file(spelling, '')
    if not os.path.isfile(broken_links):
        write_file(broken_links, '')
    if not os.path.isfile(broken_images):
        write_file(broken_images, '')


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
