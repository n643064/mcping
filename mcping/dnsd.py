import requests
import re
def query_domain(domain: str) -> list:
    try:
        r1 = requests.get("https://dnsdumpster.com/")
        if 'csrftoken' in r1.cookies:
            csrftoken = r1.cookies['csrftoken']
        else:
            csrftoken = r1.cookies['csrf']

        data = dict(targetip = domain, user = "free", csrfmiddlewaretoken=csrftoken, next='/')

        r2 = requests.post("https://dnsdumpster.com/", data=data, headers=dict(Referer="https://dnsdumpster.com/"), cookies=r1.cookies)
        r = re.compile(domain + "<br>", re.IGNORECASE)
        l = []
        for c in re.finditer(r, r2.text):
            l.append(r2.text[r2.text.rfind(">", 0, c.start())+1:c.end()-4])
        return l
    except Exception:
        return []