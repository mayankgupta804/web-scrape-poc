import os
import csv


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, "queue.txt")
    crawled = os.path.join(project_name, "crawled.txt")
    spelling = os.path.join(project_name, "spelling.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url + "," + str(0))
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(spelling):
        write_file(spelling, '')


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
           int(row[1]))for row in results)
    return set(parsed)


# Iterate through a set, each item will be a line in a file
def set_to_file(data, file_name):
    with open(file_name, "w") as out:
        csv_out = csv.writer(out)
        for row in sorted(data, key=lambda x: x[0]):
            try:
                csv_out.writerow(row)
            except UnicodeEncodeError:
                pass
