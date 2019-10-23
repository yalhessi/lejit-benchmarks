import json
import matplotlib.pyplot as plt
import fnmatch
import os

def get_files_matching_pattern(dirname, pattern):
    for filename in os.listdir(dirname):
        if fnmatch.fnmatch(filename, pattern):
            yield filename

# def read_data(filename):
#     data = json.load(open(filename))
#     return [{"name": suite["name"], "subtests": [{"name": subtest["name"], "lowerIsBetter": subtest["lowerIsBetter"], "values": subtest["replicates"] } for subtest in suite["subtests"]]} for suite in data["suites"]]

# def squash_data(data):
#     new_data = []
#     for suite in data:
#         new_suite = {"name": suite["name"]}
#         new_values = []
#         for subtest in suite["subtests"]:
#             if suite["name"] == "JetStream":
#                 subtest["values"] = [400-i for i in subtest["values"]]
#             new_values += subtest["values"]
#         new_suite["values"] = new_values
#         new_data.append(new_suite)
#     return new_data

def squash_data(data):
   for subtest in data['suites'][0]['subtests']:
       yield subtest['value']

def read_data_from_log_file(filename):
    for line in open(filename):
        if line.startswith('PERFHERDER_DATA'):
            return json.loads(line[16:])

def main():
    logdir = './logs/'
    enabled_files = list(get_files_matching_pattern(logdir, '*enabled*'))
    disabled_files = get_files_matching_pattern(logdir, '*disabled*')
    enabled_data = [squash_data(read_data_from_log_file(os.path.join(logdir, f))) for f in enabled_files[:50]]
    disabled_data = [squash_data(read_data_from_log_file(os.path.join(logdir, f))) for f in enabled_files[50:]] 
    # print([sum(x) for x in zip(*enabled_data)])
    # print([sum(x) for x in zip(*disabled_data)])
    print([x - y for x, y in zip([sum(x) for x in zip(*enabled_data)], [sum(x) for x in zip(*disabled_data)])])
    # for f in enabled_files:
    #     data = squash_data(read_data_from_log_file(os.path.join(logdir, f)))
    #     print(list(data))
    # enabled_data = squash_data(read_data('range-analysis-enabled.json'))
    # disabled_data = squash_data(read_data('range-analysis-disabled.json'))
    # for i in range(len(enabled_data)):
    #     curr_enabled_data = enabled_data[i]["values"]
    #     curr_disabled_data = disabled_data[i]["values"]
    #     plt.plot(range(400))
    #     plt.scatter(curr_enabled_data, curr_disabled_data)
    #     plt.xlabel('Range Analyis Enabled')
    #     plt.ylabel('Range Analyis Disabled')
    # plt.show()


if __name__ == "__main__":
    main()
