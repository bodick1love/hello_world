import requests
from main import *
import json
# res = requests.get("http://127.0.0.1:5000/trainers/11")
# res = requests.post("http://127.0.0.1:5000/trainers", {"idtrainer": 0, "name": "Adidas", "size": 40, "price": 400, "img_urls": [""]})
# res = requests.put("http://127.0.0.1:5000/trainers/10", {"idtrainer": 10, "name": "Adidas LITE RACER", "size": 44, "price": 40, "img_urls": [""]})
# res = requests.delete("http://127.0.0.1:5000/trainers/11")
# res = requests.get("http://127.0.0.1:5000/store/order/1")
# res = requests.post("http://127.0.0.1:5000/store/order", {"idorder": 2, "delivery_adress": "Pushkina 20", "status": "confirmation", "user_id": 1})
# res = requests.delete("http://127.0.0.1:5000/store/order/3")
# res = requests.get("http://127.0.0.1:5000/store/inventory")
# res = requests.get("http://127.0.0.1:5000/user/b_yarema")
# res = requests.post("http://127.0.0.1:5000/user", {"iduser": 2, "username": "vasya123", "full_name": "Vasyl Verastiuk", "phone_number": "380 68 011 5088", "email": "asjdjasd@gmail.com", "password": "lockedpass"})
# res = requests.put("http://127.0.0.1:5000/user/vasya123", {"iduser": 2, "username": "senya11", "full_name": "Semen Verastiuk", "phone_number": "380 68 011 5088", "email": "asjdjasd@gmail.com", "password": "lockedpass"})

# res = requests.put("http://127.0.0.1:5000/login", {"login": "b_yarema", "password": "legion"})

token = requests.post("http://127.0.0.1:5000/login", {"username": "Username0", "password": "0000"}).json()
#res = requests.delete("http://127.0.0.1:5000/user/test")
res = requests.delete("http://127.0.0.1:5000/user/test", headers={'Authorization': 'Bearer {}'.format(token)})
#res = requests.get("http://127.0.0.1:5000/user/test")
#res = requests.post("http://127.0.0.1:5000/user", {"iduser": 1, "username": "test", "full_name": "Vasyl Verastiuk", "phone_number": "380 68 011 5088", "email": "asjdjasd@gmail.com", "password": "test"})
#res = requests.post("http://127.0.0.1:5000/user", {"iduser" : 1,"username" : "b_yarema", "full_name" : "bohdan_yarema", "phone_number" : "1234", "email" : "b@gmail.com", "password" : 1111})
print(token)
print(res.json())
