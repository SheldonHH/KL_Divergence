import requests

def obtainListofbgePercent():
  # TODO: replace "http://0.0.0.0" to server IP
  bgePercent_url = 'http://0.0.0.0:5920/bgePercent' # benchmark, gaussian Entropy Percentage
  inputDicts = {"user_1": [1, 10000], "user_2": [10000, 20000], "user_3": [20000, 30000], "user_4": [30000,40000], "user_5": [40000,50000], "user_6": [50000,60000]}
  try:
    x = requests.post(bgePercent_url, json = inputDicts)
    x.raise_for_status()
  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)

  
  return list(x)[0],list(x)[1]


