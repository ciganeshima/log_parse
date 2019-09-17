# -*- encoding: utf-8 -*-
import re
import datetime
from collections import Counter
from datetime import datetime
from collections import defaultdict


def get_logs(line):
    if re.fullmatch(r'\[\d\d/\w{3}/\d{4}\s\d\d:\d\d:\d\d\]\s\"\w+\s\S+\s\S+\"\s\d+\s\d+\s', line):
        return True
    return False


def www(ignore_www, URL):
    if ignore_www:
        if URL.startswith('www.'):
            return URL[4:]
    return URL


def start(start_at, line):
    if start_at:
        data = datetime.strptime(line[1:line.index(']')], '%d/%b/%Y %X')
        start_at = datetime.strptime(start_at,'%d/%b/%Y %X')
        if data < start_at:
            return True
    return False


def stop(stop_at, line):
    if stop_at:
        data = datetime.strptime(line[1:line.index(']')], '%d/%b/%Y %X')
        stop_at = datetime.strptime(stop_at,'%d/%b/%Y %X')
        if data > stop_at:
            return True
    return False


def ignore(ignore_files, URL):
    if ignore_files:
        beg = URL.rfind('.')
        postfix = URL[beg + 1:]
        if postfix.isalpha() and 3 <= len(postfix) <= 4:
            return True
        return False


def request(request_type,line):
    if request_type:
        start = line.find('\"')
        end = line.find(' ', start+1)
        type = line[start+1: end]
        if request_type == type:
            return False
        return True
    return False


def find_url(log):
    start = log.find('http')
    end = log.find(' ', start+1)
    url = log[start: end]
    url = url.replace('https://', '')
    url = url.replace('http://', '')
    pos = url.find('?')
    url = url[0: pos]
    return url


def urls_ignore(ignore_urls, URL):
    for ign_url in ignore_urls:
        if URL == ign_url:
            return True
        else:
            return False


def slowest(d, line ,URL):
    time = int(line[line.rfind(" ") + 1:])
    d[URL] = [1, time]

def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):
    log_dict = defaultdict()
    counter = Counter()
    f = open('C:\\Users\\Acer\\PycharmProjects\\log_parse\\log.log.txt')
    for line in f:
        if get_logs(line):
            if request(request_type, line):
                continue

            if start(start_at, line):
                continue

            if stop(stop_at, line):
                break

            URL = find_url(line)

            if ignore(ignore_files, URL):
                continue

            if urls_ignore(ignore_urls, URL):
                continue

            URL = www(ignore_www, URL)

            if slow_queries:
                slowest(log_dict, line, URL)
            else:
                counter[URL] += 1

    if slow_queries:
        if len(log_dict) == 0:
            return []
        new_list = []
        for value in log_dict.values():
            new_list.append(int(value[1]) // value[0])

        new_list = sorted(new_list, reverse=True)
        if len(new_list) >= 5:
            return [new_list[i] for i in range(5)]
        else:
            return [new_list[i] for i in range(len(new_list))]
    else:
        return [item[1] for item in counter.most_common(5)]


def main():
        print(parse())


if __name__ == '__main__':
        main()

