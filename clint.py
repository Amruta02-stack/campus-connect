import time
from datetime import date, timedelta
import requests
URL = "http://127.0.0.1:8001"
tag = str(int(time.time()))          

def show(label, r):
    print(label, "->", r.status_code, r.json())
def login(email, password):
    r = requests.post(URL + "/auth/login", json={"email": email, "password": password})
    return r.json()


# ---- admin (created automatically when the app starts) ----
admin = login("admin@campus.com", "admin123")
admin_h = {"token": admin["access_token"]}

# E1 create coordinator
coord_mail = "coord" + tag + "@campus.com"
r = requests.post(URL + "/admin/coordinators", headers=admin_h,
                  json={"username": "coord" + tag, "email": coord_mail, "password": "1234"})
show("E1 create coordinator (201)", r)
coord_id = r.json()["user"]["id"]
coord_h = {"token": login(coord_mail, "1234")["access_token"]}

# E2 create club
r = requests.post(URL + "/clubs", headers=admin_h,
                  json={"name": "Coding Club " + tag, "description": "We code", "category": "tech", "coordinator_id": coord_id})
show("E2 create club (201)", r)
club_id = r.json()["id"]

# A1 register student, A2 login
stu_mail = "stu" + tag + "@campus.com"
show("A1 register (201)", requests.post(URL + "/auth/register",
     json={"username": "stu" + tag, "email": stu_mail, "password": "1234"}))
tokens = login(stu_mail, "1234")
stu_h = {"token": tokens["access_token"]}

# A3 refresh
r = requests.post(URL + "/auth/refresh", headers={"refresh-token": tokens["refresh_token"]})
show("A3 refresh (200)", r)

# E3, E4, E5
show("E3 all clubs (200)", requests.get(URL + "/clubs", headers=stu_h))
show("E4 one club (200)", requests.get(URL + f"/clubs/{club_id}", headers=stu_h))
show("E5 update club (200)", requests.patch(URL + f"/clubs/{club_id}", headers=coord_h, json={"description": "We code every Friday"}))

# E6 join, E8 members, E7 approve
r = requests.post(URL + f"/clubs/{club_id}/join", headers=stu_h)
show("E6 join club (201)", r)
membership_id = r.json()["id"]
show("E8 members (200)", requests.get(URL + f"/clubs/{club_id}/members", headers=coord_h))
show("E7 approve (200)", requests.patch(URL + f"/clubs/{club_id}/members/{membership_id}", headers=coord_h, json={"status": "approved"}))

# E9 create event, E10 list events
tomorrow = str(date.today() + timedelta(days=1))
r = requests.post(URL + f"/clubs/{club_id}/events", headers=coord_h,
                  json={"title": "Hackathon", "description": "24 hour hack", "venue": "Hall A", "date": tomorrow, "capacity": 1})
show("E9 create event (201)", r)
event_id = r.json()["id"]
show("E10 all events (200)", requests.get(URL + "/events", headers=stu_h))

# E11 register, E14 participants, E13 attendance, E15 history
show("E11 register event (201)", requests.post(URL + f"/events/{event_id}/register", headers=stu_h))
show("E14 participants (200)", requests.get(URL + f"/events/{event_id}/participants", headers=coord_h))
stu_id = requests.get(URL + f"/events/{event_id}/participants", headers=coord_h).json()[0]["student_id"]
show("E13 attendance (200)", requests.patch(URL + f"/events/{event_id}/attendance", headers=coord_h, json={"student_id": stu_id}))
show("E15 history (200)", requests.get(URL + "/students/me/participation", headers=stu_h))

# E12 cancel (409 because attendance is already marked, so we test it on a second event)
r = requests.post(URL + f"/clubs/{club_id}/events", headers=coord_h,
                  json={"title": "Workshop", "description": "Python", "venue": "Lab 2", "date": tomorrow, "capacity": 10})
event2 = r.json()["id"]
requests.post(URL + f"/events/{event2}/register", headers=stu_h)
show("E12 cancel registration (200)", requests.delete(URL + f"/events/{event2}/register", headers=stu_h))

# ---- error checks ----
print("--- error checks ---")
print("duplicate email        (409):", requests.post(URL + "/auth/register", json={"username": "x", "email": stu_mail, "password": "1234"}).status_code)
print("wrong password         (401):", requests.post(URL + "/auth/login", json={"email": stu_mail, "password": "wrong"}).status_code)
print("no token               (401):", requests.get(URL + "/clubs").status_code)
print("student creates club   (403):", requests.post(URL + "/clubs", headers=stu_h, json={"name": "a", "description": "b", "category": "c", "coordinator_id": 1}).status_code)
print("join club twice        (409):", requests.post(URL + f"/clubs/{club_id}/join", headers=stu_h).status_code)
print("register event twice   (409):", requests.post(URL + f"/events/{event_id}/register", headers=stu_h).status_code)
print("club not found         (404):", requests.get(URL + "/clubs/9999", headers=stu_h).status_code)
print("bad email              (422):", requests.post(URL + "/auth/register", json={"username": "x", "email": "abc", "password": "1234"}).status_code)

# event full: second student tries the capacity-1 event
other = "other" + tag + "@campus.com"
requests.post(URL + "/auth/register", json={"username": "other", "email": other, "password": "1234"})
other_h = {"token": login(other, "1234")["access_token"]}
print("event full             (409):", requests.post(URL + f"/events/{event_id}/register", headers=other_h).status_code)