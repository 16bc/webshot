# Webshot manual
#### Script goes to webservices on ip-addresses from file and take screenshots.
It is created as useful addition to the <b>Nmap</b> and <b>masscan</b> utilities. Tested on Ubuntu 18.04 & Python 3.7

* Script based on <b>Selenium</b>, so you need have installed <b>Selenium WebDriver</b> first.  
* Before running script, open <b>webshot.py</b> in editor and check or change variables in the header.  
* Make sure you have <b>.json</b> file generated from Nmap, Masscan (use `-oJ` key), or same utilities, with json-format something like this:
```
{ "ip": "xxx.xxx.xxx.xxx", "ports":[{"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 61}]},
{ "ip": "xxx.xxx.xxx.xxx", "ports":[{"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 60}]},
{ "ip": "xxx.xxx.xxx.xxx", "ports":[{"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 61}]},
...
```

If you want use custom list-file with IPs, just edit <i>parse_hosts()</i> function so it return list with IPs.
