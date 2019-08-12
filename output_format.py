import collections
import csv
import json

from command_line_arguments import args
from variables import logging, top_size


def console_json_csv_output(wds):
    logging.debug(args)
    if args.report_format == 'console':
        print('total %s words, %s unique' % (len(wds), len(set(wds))))
        for word, occurence in collections.Counter(wds).most_common(top_size):
            print(word, occurence)

    if args.report_format == 'json':
        dict_for_json = {}
        for word, occurence in collections.Counter(wds).most_common(top_size):
            dict_for_json.update({word[0]: (word[1], occurence)})
        with open(args.output, "w") as write_file:
            json.dump(dict_for_json, write_file)

    if args.report_format == 'csv':
        list_for_csv = []
        for word, occurence in collections.Counter(wds).most_common(top_size):
            list_for_csv.append([word[0], word[1], occurence])
        with open(args.output, "w") as write_file:
            writer = csv.writer(write_file, delimiter=',')
            for line in list_for_csv:
                writer.writerow(line)
