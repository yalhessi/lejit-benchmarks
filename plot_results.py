import json
import matplotlib.pyplot as plt
import fnmatch
import os

def get_files_matching_pattern(dirname, pattern):
    for filename in os.listdir(dirname):
        if fnmatch.fnmatch(filename, pattern):
            yield filename

def squash_data(data):
   for subtest in data['suites'][0]['subtests']:
       yield subtest['value']

def read_data_from_log_file(filename):
    for line in open(filename):
        if line.startswith('PERFHERDER_DATA'):
            return json.loads(line[16:])

def main():
    logdir = './logs/'
    enabled_files = get_files_matching_pattern(logdir, '*enabled*')
    disabled_files = get_files_matching_pattern(logdir, '*disabled*')
    enabled_data = [squash_data(read_data_from_log_file(os.path.join(logdir, f))) for f in enabled_files]
    disabled_data = [squash_data(read_data_from_log_file(os.path.join(logdir, f))) for f in disabled_files] 
    # print([x - y for x, y in zip([sum(x) for x in zip(*enabled_data)], [sum(x) for x in zip(*disabled_data)])])
    
if __name__ == "__main__":
    main()
