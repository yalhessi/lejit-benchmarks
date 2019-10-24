import json
import matplotlib.pyplot as plt
import fnmatch
import os
import statistics
from tabulate import tabulate

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

def read_test_data(data):
    res = {}
    tests = data['suites'][0]['subtests']
    for t in tests:
        res[t['name']] = t['value']
    return res

def test_data_to_stats(tests):
    stats = {}
    for t in tests:
        if t:
            parsed = read_test_data(t)
            for b in parsed.keys():
                if b in stats:
                    stats[b].append(parsed[b])
                else:
                    stats[b] = [parsed[b]]
    return stats

def print_stats(stats):
    for bench in stats.keys():
        print bench + ":"
        print "\tmin: " + str(min(stats[bench]))
        print "\tmax: " + str(max(stats[bench]))
        print "\tmean: " + str(statistics.mean(stats[bench]))
        print "\tmedian: " + str(statistics.median(stats[bench]))
        print "\tstdev: " + str(statistics.stdev(stats[bench]))
        print ""
    
def main():
    logdir = './logs/'
    enabled_files = get_files_matching_pattern(logdir, '*enabled*')
    disabled_files = get_files_matching_pattern(logdir, '*disabled*')
    enabled_data = [read_data_from_log_file(os.path.join(logdir, f)) for f in enabled_files]
    disabled_data = [read_data_from_log_file(os.path.join(logdir, f)) for f in disabled_files] 
    enabled_stats = test_data_to_stats(enabled_data)
    disabled_stats = test_data_to_stats(disabled_data)

    for bench in enabled_stats.keys():
        table = [[f.__name__, f(enabled_stats[bench]), f(disabled_stats[bench])]
                        for f in [min, max, statistics.mean, statistics.median, statistics.stdev]]
        print bench + ":"
        print tabulate(table, headers=['stat', 'enabled', 'disabled'])
        print ""
    
if __name__ == "__main__":
    main()
