import json
from sensors import S
json.dump([{"n":x["n"],"title":x["title"],"code":x.get("code")} for x in S],open("sensors.json","w",encoding="utf-8"))
print(len(S),'sensors;',sum(1 for x in S if x.get("code")),'with code;',min(len(x["examples"]) for x in S),'min examples')
