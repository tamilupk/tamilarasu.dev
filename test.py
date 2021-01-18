import requests

r =requests.get('https://www.tamilarasu.dev')

if r.status_code == 200:
    print('Test passed')
else:
    print('Test failed')
    raise Exception()