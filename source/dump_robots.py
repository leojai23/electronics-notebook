import json
from robots import R
json.dump([{"n":r["n"],"title":r["title"],"code":r["code"]} for r in R],open("robots.json","w",encoding="utf-8"))
print(len(R), "exercises;", sum(1 for r in R if r["code"]), "with code")
