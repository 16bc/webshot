#
# Script going to addresses from file and take screenshots
# 
from multiprocessing import Process, Queue, cpu_count
from selenium import webdriver
import logging
import os
import json
from time import sleep
#########################################################################################
#                              VARIABLES IN THE HEADER
#########################################################################################
screens_directory = './scrs/'
hosts_file = 'ips.json'  # Nmap оr Masscan output JSON file name
log_filename = "log.txt"
count_of_workers = cpu_count()  # Count of workers.
page_load_timeout = 5
wait_on_page = 1
take_screenshot_anyway = True
''' True - will take scr. even if page load not complete in the <page_load_timeout> time;
    False - do not take scr. of such pages. May be useful if generated many "white pages"
'''
def driver(): return webdriver.Firefox(executable_path='./driver/geckodriver')
# Change to webdriver.Chrome() if need.
#########################################################################################


def say(i, text):
    """
    Colorized & personalized messages from workers
    :param i: Worker id
    :param text: Message
    """
    colors = [30, 32, 34, 35, 36, 93, 30, 32, 34, 35, 36, 93]
    return log.info(f"\033[{colors[i]}m Worker-{i} said: {text}")


def parse_hosts(hosts_file):
    hosts = []
    with open(hosts_file, 'r') as file:
        lines = file.readlines()[:-1]
    for line in lines:
        hosts.append(json.loads(line[:-2])['ip'])
    log.info(f'Addresses loaded. Addresses count is:{len(hosts)}')
    return hosts


def selenium_task(id, worker, host):
    url = f'http://{host}/'
    filename = f"{screens_directory}{host}.png"
    say(id, f"☐ Begining to load host {host}...")
    try:
        worker.get(url)
        sleep(wait_on_page)
        worker.get_screenshot_as_file(filename)
        say(id, f"(✅ 📷) I'm successfully load and screen {host}")
    except:
        if take_screenshot_anyway:
            worker.get_screenshot_as_file(filename)
            say(id, f"(❌ 📷) Page load not complite from {host}, but screenshot was taken.")
        else:
            say(id, f"(❌) Page load not complite from {host}. No screen.")


def selenium_queue_listener(hosts_q, workers_q):
    log.info("Selenium func worker started")
    while True:
        current_host = hosts_q.get()
        if current_host == 'STOP':
            log.warning("STOP encountered, killing worker process")
            hosts_q.put(current_host)
            break
        else:
            # Get the ID of any currently free workers from the worker queue
            worker_id = workers_q.get()
            selenium_task(worker_id, selenium_workers[worker_id], current_host)
            workers_q.put(worker_id)
    return


if __name__ == '__main__':

    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format=FORMAT)
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

    log.info(f"Try to create {count_of_workers} workers")
    worker_ids = list(range(count_of_workers))
    for worker_id in worker_ids:
        workers_queue.put(worker_id)

    selenium_workers = {}
    try:
        for i in worker_ids:
            selenium_workers[i] = driver()
            selenium_workers[i].set_page_load_timeout(page_load_timeout)
            say(i, f"I born! I'm happy and ready to work!")
    except:
        log.error('Create workers error! Be sure you have installed Selenium WebDriver \
and gecodriver path in header is valid.')

    selenium_processes = [Process(target=selenium_queue_listener,
                                 args=(hosts_queue, workers_queue)) for _ in worker_ids]
    for p in selenium_processes:
        p.daemon = True
        p.start()

    for p in selenium_processes:
        p.join()

    # Quit all the web workers elegantly in the background
    log.info("\033[31m ---Dismissing web workers---")
    for w in selenium_workers.values():
        w.quit()
