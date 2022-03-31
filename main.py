import requests as rq
import xml.dom.minidom as minidom
import re

wikiregex = '^https://[a-z]+.wikipedia.org/wiki/[^ ]+'
startpoint = input('Start article: ')

while not re.match(wikiregex, startpoint):
    print('Sorry, but your input doesn\'t match the regex!')
    startpoint = input('Start article: ')

mode = input('''Scanning mode:
\tfind (start from given article and stop on another one)
\tnormal (normal scanning) ''')

while not mode in ['normal', 'find']:
    print(f'Unknown option')
    mode = input('Normal or find? ')

endpoint = ''
if mode == 'find':
    endpoint = input('End article: ')
    while not re.match(wikiregex, startpoint):
        print('Sorry, but your input doesn\'t match the regex!')
        endpoint = input('End article: ')

dist = {}
visited = []
queue = [startpoint]
count = 0
base = startpoint[:-(len(startpoint.split('/')[len(startpoint.split('/'))-1])+5)]
dist[startpoint] = 0
path = {}
path[startpoint] = [startpoint[len(base) + 5:]]


def visit(url):
    global count
    global endpoint

    count += 1
    print(f'Scanning: {url}')
    document = minidom.parseString(rq.get(url).text)
    links = document.getElementsByTagName('a')

    conn = 0
    for link in links:
        href = link.getAttribute('href')
        if re.match('/wiki/.*', href) and not ':' in href and not href in visited and not url.endswith(href):
            visited.append(href)
            queue.insert(0, href)
            print(f'Added to queue: {base + href[1:]}')
            conn += 1
            dist[base + href[1:]] = dist[url] + 1

            curr_path = path[url].copy()
            curr_path.append(href[6:])
            path[base + href[1:]] = curr_path
            
            if (base + href[1:] == endpoint):
                print(f'Found {endpoint}!')
                print(f'Scanned {count} articles')
                print(f'The shortest path from {startpoint} to {endpoint} is: {dist[url] + 1}')
                print(f'Path: {" -> ".join(curr_path)}')
                return

    print(f'{url} has {conn} connected articles')
    print(f'Currently queued: {len(queue)}')

    queue.pop()
    if len(queue) == 0:
        # this will never happen xD
        print(f'Finished! Scanned {count} articles')
    else:
        visit(base + queue[len(queue) - 1][1:])


visit(queue[0])
