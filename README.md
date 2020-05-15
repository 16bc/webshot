# 📸 WᴇʙSʜᴏᴛ
#### Script goes to webservices on ip-addresses from file and take screenshots.
It is created as useful addition to <b>masscan</b> utility. Tested on Ubuntu 18.04 & Python 3.7

* Script base on <b>Selenium</b>, so you need have installed <b>Selenium WebDriver</b> first.  
[Link to Selenium Webdriver setup manual](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/)
* Before running script, open <b>webshot.py</b> in editor and check or change variables in the header.  
* Make sure you have <b>.json</b> file generated from Masscan (use `-oJ` key), or same utilities, with json-format something like this:
```
{ "ip": "xxx.xxx.xxx.xxx", "ports":[{"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 61}]},
{ "ip": "xxx.xxx.xxx.xxx", "ports":[{"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 60}]},
{ "ip": "xxx.xxx.xxx.xxx", "ports":[{"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 61}]},
...
```
Script set up to firefox, you may change it in the header.  
If you want use custom list-file with IPs, just edit <i>parse_hosts()</i> function so it return list with IPs.
