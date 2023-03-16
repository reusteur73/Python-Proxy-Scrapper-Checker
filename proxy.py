import requests, json
from checker import ProxyChecker
import threading

###### ARGS ######
country = "US" #COUNTRY PROXY
limit = "100" #LIMIT PROXY LIST
checker = ProxyChecker(save_to_file="path/to/file.txt") #Optional output file full path, remove args if unwanted.
# checker = ProxyChecker() #In case of non-output file.

link = "https://proxylist.geonode.com/api/proxy-list?limit="+limit+"&page=1&sort_by=lastChecked&sort_type=desc&country="+country
data = requests.get(link).text
fix = json.loads(data)

output = []

result = {
    "result": {
        "Region": country,
        "proxylist": []
    }
}
for x in fix["data"]:
    ip = x["ip"]
    port = x["port"]
    result["result"]["proxylist"].append(ip+":"+port)
    output.append(ip+":"+port)
print(str(json.dumps(result,indent=4)))

class ProxyCheckerThread(threading.Thread):
    def __init__(self, proxy, checker):
        threading.Thread.__init__(self)
        self.proxy = proxy
        self.checker = checker
    
    def run(self):
        r = self.checker.check_proxy(self.proxy)
        if r is not None:
            print(r)

threads = []
for proxy in output:
    t = ProxyCheckerThread(proxy, checker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
