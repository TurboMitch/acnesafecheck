#!/usr/bin/env python3
"""Submit all sitemap URLs to IndexNow (Bing, Yandex, etc.). Run after deploy.
Usage: python3 indexnow_submit.py
"""
import json, re, urllib.request

KEY = "1d1ec46e415be608062d580613dd40b797748854c4f6aa379c211e321fd621eb"
HOST = "acnesafecheck.com"
ENDPOINT = "https://www.bing.com/indexnow"  # Bing accepts the shared IndexNow key; the generic aggregator can 403

urls = re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml", encoding="utf-8").read())
# IndexNow accepts up to 10,000 URLs per request
payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/{KEY}.txt",
    "urlList": urls,
}
req = urllib.request.Request(
    ENDPOINT, data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req) as r:
        print(f"IndexNow: submitted {len(urls)} URLs — HTTP {r.status}")
except Exception as e:
    print(f"IndexNow submit failed: {e}")
