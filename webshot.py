'''
Script going to addresses from file and take screenshots
'''
from threading import Thread
from multiprocessing import Queue, cpu_count
from selenium import webdriver
import logging
import os
import json

#########################################################################################
#                                      VARIABLES
#########################################################################################
screens_directory = './scrs/'
hosts_file = 'scan_result.json'  # Nmap оr Masscan output JSON file name
count_of_workers = cpu_count()  # Count of workers.
page_load_timeout = 5
take_screenshot_anyway = True
''' True - will take scr. even if page load not complete in the <page_load_timeout> time;
    False - do not take scr. of such pages.'''
#########################################################################################


def say(i, text):
    colors = [30, 32, 34, 35, 36, 93]
    return log.info(f"\033[{colors[i]}m Worker-{i} said: {text}")


def parse_hosts(hosts_file):
    hosts = []
    with open(hosts_file, 'r') as file:
        lines = file.readlines()[:-1]
    for line in lines:
        hosts.append(json.loads(line[:-2])['ip'])
    log.info(f'Список адресов загружен. Количество адресов:{len(hosts)}')
    return hosts


def selenium_task(id, worker, host):
    url = f'http://{host}/'
    filename = f"{screens_directory}{host}.png"
    try:
        say(id, f"Begining to load host {host}...")
        try:
            worker.get(url)
            worker.get_screenshot_as_file(filename)
            say(id, f"I'm successfully load and screen {host}")
        except:
            say(id, f"Page load dont complite from {host}")
            if take_screenshot_anyway:
                worker.get_screenshot_as_file(filename)
    except:
        log.warning(f"Extremely strange Error on load {host}!")


def selenium_queue_listener(hosts_q, workers_q):
    log.info("Selenium func worker started")
    while True:
        current_host = hosts_q.get()
        if current_host == 'STOP':
            log.warning("STOP encountered, killing worker thread")
            hosts_q.put(current_host)
            break
        else:
            # Get the ID of any currently free workers from the worker queue
            worker_id = workers_q.get()
            selenium_task(worker_id, selenium_workers[worker_id], current_host)
            workers_q.put(worker_id)
    return


if __name__ == '__main__':

    logging.basicConfig(filename="log.log", level=logging.INFO, )
    log = logging.getLogger("logger")
    log.addHandler(logging.StreamHandler())

    if not os.path.exists(screens_directory):
        os.makedirs(screens_directory)

    hosts = parse_hosts(hosts_file)
    hosts.append('STOP')

    hosts_queue = Queue()
    workers_queue = Queue()

    log.info("Adding hosts to hosts queue")
    for h in hosts:
        hosts_queue.put(h)

    log.info("Create workers")
    worker_ids = list(range(count_of_workers))
    for worker_id in worker_ids:
        workers_queue.put(worker_id)

    selenium_workers = {}
    for i in worker_ids:
        selenium_workers[i] = webdriver.Firefox()
        selenium_workers[i].set_page_load_timeout(page_load_timeout)
        say(i, f"I born! I'm so happy! Give me some work!")

    selenium_processes = [Thread(target=selenium_queue_listener,
                                 args=(hosts_queue, workers_queue)) for _ in worker_ids]
    for p in selenium_processes:
        p.daemon = True
        p.start()

    for p in selenium_processes:
        p.join()

    # Quit all the web workers elegantly in the background
    log.info("\033[{colors[31]}m Tearing down web workers")
    for w in selenium_workers.values():
        w.quit()
