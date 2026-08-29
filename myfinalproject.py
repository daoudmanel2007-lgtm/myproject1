from abc import ABC, abstractmethod
def gymmenu():
    print("~" * 50)
    print("     THE MENU of the gym FitZone ")
    print("~" * 50)
    print("1.new membership")
    print("2.add a new session")
    print("3.book a session")
    print("4.cancel a booking")
    print("5.calculate the price of the session")
    print("6.search for a session")
    print("7.display a member's booked session")
    print("8.display overall statistics")
    print("9.automatic monthly report")
    print("10.EXIT cleanly")
    print("~" * 50)
    print("if its your firt time you need to pay extra 500DA as the card fee ")
 
class Utils:
    idcounter = 0
 
    @staticmethod
    def generateId():
        Utils.idcounter += 1
        return "FTZALG2026" + str(Utils.idcounter)
    @staticmethod
    def pricediscount(price, age, first_time):
        if first_time :
            price += 500
        if age < 18 or age >= 60:
            price = price * 0.85
        return price
 
class Session(ABC):
    def __init__(self, name, period, coach, sessionID):
        self.name = name
        self.period = period
        self.coach = coach
        self.sessionID = sessionID
        self.capacity = self.maxcapacity()
        self.participants = []
    @abstractmethod
    def calculate_price(self):
      pass
    @abstractmethod
    def maxcapacity(self):
        pass
    def __str__(self):
     remaining = self.capacity - len(self.participants)
     return (
        "Session ID: " + self.sessionID +
        " | Session: " + self.name +
        " | Coach: " + self.coach +
        " | Period: " + self.period +
        " | Booked: " + str(len(self.participants)) +
        "/" + str(self.capacity) +
        " | Remaining seats: " + str(remaining)
     )
            
    def __eq__(self, other):
      try:
        return self.sessionID == other.sessionID
      except:
        return False
 
    def __len__(self):
        return len(self.participants)
 
    def check_fullness(self):
        return len(self.participants) >= self.capacity
 
class Groupclass(Session):
    def __init__(self, IDsession, name, period, coach, basecoast):
      super().__init__(name, period, coach, IDsession)
      self.basecoast = basecoast
      self.waitelist = []
      self.category="group"
 
    def maxcapacity(self):
        return 8
    def calculate_price(self):
     try:
         return self.basecoast / len(self.participants)
     except ZeroDivisionError:
         return self.basecoast
 
 
class Personaltraining(Session):
    def __init__(self, name, period, coach, sessionID, hourly_rate):
     super().__init__(name, period, coach, sessionID)
     self.hourly_rate = hourly_rate
     self.category="personal"
 
    def maxcapacity(self):
        return 1
 
    def calculate_price(self):
        return self.hourly_rate
 
 
class Member:
    def __init__(self, name, fname, memberID, age):
        self.name = name
        self.fname = fname
        self.memberID = memberID
        self.age = age
        self.bookings = []
        self.first_time = True
 
    def __len__(self):
        return len(self.bookings)
 
    def book(self, session):
        if session in self.bookings:
            return "you have already booked this session"
 
        if session.check_fullness():
            if session.category == "group":
                if self in session.waitelist:
                    return "you are already on the waiting list for this session"
                session.waitelist.append(self)
                return "This class is full but you are now on the waiting list"
 
            return "This session is already full"
        session.participants.append(self)
        self.bookings.append(session)
        return "your booking is confirmed"
 
    def cancel(self, session):
        if session not in self.bookings:
            return "this session is not in your booking system"
 
        self.bookings.remove(session)
        session.participants.remove(self)
        if session.category == "group" and len(session.waitelist) > 0:
            x = session.waitelist.pop(0)
            session.participants.append(x)
            x.bookings.append(session)
            return "mr/ms " + x.name + " " + x.fname + " you are removed automtically from  the waitlist"
 
        return "booking cancelled successfully"

    
class Gym:
    totbooking = 0
    def __init__(self):
        self.session = {}
        self.members = {}

    def loginnewclient(self, name, fname, age):
        yourID = Utils.generateId()
        yourmembership = Member(name, fname, yourID, age)
        self.members[yourID] = yourmembership
        return yourmembership

    def addsession(self, session):
        self.session[session.sessionID] = session
        return session

    def book_session(self, memberID, sessionID):
        if memberID not in self.members:
            return "this member isnt in this list"

        if sessionID not in self.session:
            return "session unfound in our list"

        member = find_member(self.members, memberID)
        session = find_session(self.session, sessionID)

        result = member.book(session)
        if result == "your booking is confirmed":
            Gym.totbooking += 1
        return result

    def cancel_booking(self, memberID, sessionID):
        if memberID not in self.members:
            return "this member is not in this list"
        if sessionID not in self.session:
            return "this session is not in my list"
        member = find_member(self.members, memberID)
        session = find_session(self.session, sessionID)
        result = member.cancel(session)
        if result == "booking cancelled successfully":
         if Gym.totbooking > 0:
             Gym.totbooking -= 1
        return result

    def search(self, sessiontype, trainer):
        results = []
        for session in self.session.values():
            matches = True
            if trainer != "":
                if trainer.lower() not in session.coach.lower():
                    matches = False
            if sessiontype != "":
                if session.category != sessiontype:
                    matches = False
            if matches:
                results.append(session)
        return results

    def statistics(self):
        print("~~~~~~~~~~~~OUR STATISTICS OF THE FITZONE GYM~~~~~~~~~~~~~~")
        print("our statistics :")
        print("the total number of members :", len(self.members))
        print("the total number of session :", len(self.session))
        print("the total number of bookings :", Gym.totbooking)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        popular = None
        bestbooking = 0
        for session in self.session.values():
            if len(session) > bestbooking:
                popular = session
                bestbooking = len(session)
        if popular is not None:
            print("the most popular session is:", popular.name,
                  "with", bestbooking, "bookings")
        else:
            print("there is no session booked")
        print("~~~~~~~~~~~~POPULARITY RANKING~~~~~~~~~~~~")
        ranking = []
        for session in self.session.values():
            ranking.append((len(session), session.name))
        for i in range(len(ranking)):
          for j in range(i + 1, len(ranking)):
            if ranking[j][0] > ranking[i][0]:
               ranking[i], ranking[j] = ranking[j], ranking[i]
        position = 1
        for bookings, name in ranking:
            print(position, "~~", name, "~~", bookings, "bookings")
            position += 1
    def monthly_report(self):
        print("~~~~~~~~~~~~~~~~~~MONTHLY REPORT~~~~~~~~~~~~~~~~~~")
        if len(self.members) == 0:
            print("there is no members registered yet")
            return
        for member in self.members.values():
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("member:", member.name, member.fname)
            print("ID:", member.memberID)
            if len(member) == 0:
                print("this member has no bookings this month")
                continue
            for session in member.bookings:
                price = session.calculate_price()
                finalprice = Utils.pricediscount(
                    price,
                    member.age,
                    member.first_time
                )
                if member.first_time:
                   member.first_time = False
                print("the session:", session.name,"by the coach:", session.coach,"and it price:", finalprice, "DA")   

def find_member(membersdict, memberID):
    if memberID in membersdict:
        return membersdict[memberID]
    else:
        return "this member isnt in this list"
def find_session(sessions_dict, session_id):
    if session_id in sessions_dict:
        return sessions_dict[session_id]
    else:
        return "session unfound in our list"
 
        
def asknumber(question): 
    maxtries = 3
    tries = 0
    while tries < maxtries:
        text = input(question)
        try:
            return int(text)
        except ValueError:
            tries = tries + 1
            print("you inter a false input please enter a digit,you have only",str(tries),"try from 3 tries")
    print("please go to the main menu if there is a lot of miss try")
    return None 
 
def newmembership_menu(gym):
    print("_________THE NEW MEMBERSHIP___________")
    name = input("enter yout first  name: ")
    fname = input("enter your family name: ")
    age = asknumber("your age: ")
    print("thank you for the discreption")
    if age is None:
        return
    while age <= 0 or age > 120:
        print("please enter a valid age between 1 and 120")
        age = asknumber("your age: ")
        if age is None:
            return
    member = gym.loginnewclient(name, fname, age)
    print(" Our new mamber:",member.name,"" ,member.fname,"wellcome to the FITZONE,your ID: ",member.memberID)
    print("here is our list of coaches:")
    for cid in coaches:
        print(cid, ":", coaches[cid]["name"], "  ", coaches[cid]["classes"])
 
def addsession_menu(gym):
    print("~~~~~~~~adding a new session~~~~~~~~~~~~")
    name = input("enter your class's name: ")
 
    print("choose your training period:")
    print("1. morning")
    print("2.afternoon")
 
    try:
        period_choice = int(input("Choose the period you want,type 1 or2: "))
        if period_choice == 1:
            period = "morning"
        elif period_choice == 2:
            period = "afternoon"
        else:
            print("Error: Please choose 1 or 2   only")
            return
    except ValueError:
        print("there is an error you did not type a number")
        return
 
    print("choose your coach:")
    for cid in coaches:
        print(cid, ":", coaches[cid]["name"], "   ", coaches[cid]["classes"])
 
    coachID = input("enter the coach's ID: ")
    if coachID not in coaches:
        print("this coach ID is not in our list")
        return
    coach = coachID + " - " + coaches[coachID]["name"]
    print("pease choose the way of training:")
    print("1. group ")
    print("2. personal training")
 
    try:
        choice = int(input("Choose your train path: "))
        if choice != 1 and choice != 2:
            print("Error: Please choose 1 or 2 only ")
            return
    except ValueError:
        print("there is an error you did not type a number")
        return
 
    newID = Utils.generateId()
 
    if choice == 1:
        try:
            basecoast = float(input("Base cost for this class is: "))
        except ValueError:
            print("there is an error you did not type a number")
            return
        newsession = Groupclass(newID, name,period, coach, basecoast)
 
    elif choice == 2:
        try:
            hourly_rate = float(input("the hourly rate:: "))
        except ValueError:
            print("there is an error you did not type a number")
            return
        newsession = Personaltraining(name, period, coach, newID, hourly_rate)
    gym.addsession(newsession)
    print("the session is added from the  ID:", newID)
 
 
def booksession_menu(gym):
    print("~~~~~~~~~BOOKING THE SESSION~~~~~~~~~~~~")

    print("Available sessions:")
    for session in gym.session.values():
        print(session)

    memberID = input("Please enter your Member ID: ")
    sessionID = input("Please enter the Session ID: ")

    result = gym.book_session(memberID, sessionID)
    print(result)
 
 
def cancelbooking_menu(gym):
    print("~~~~~~~~~~~~~~~~~~CALCELING THE BOOKING~~~~~~~~~~~~~~")
    memberID = input("please input your member ID: ")
    sessionID = input("please input your session ID: ")
    result = gym.cancel_booking(memberID, sessionID)
    print(result)
 
 
def price_menu(gym):
    print("the session price:")
    sessionID = input("iput please your session ID: ")
    memberID = input("Your member ID : ")

    if sessionID not in gym.session:
        print("this session is unfound in our system")
        return

    session = find_session(gym.session, sessionID)
    price = session.calculate_price()

    if memberID in gym.members:
        member = find_member(gym.members, memberID)
        price = Utils.pricediscount(price, member.age, member.first_time)

        if member.first_time == True:
            print("sice its your first time is out gym you will add 500 DA for the card fee")
           
    else:
        print("this member isnt in this list")
        return

    print("this session will coast you:" + str(price))
 
    
def search_menu(gym):
    print("~~~~~~~~~~~~~~~~~SEARCH FOR YOUR SESSION~~~~~~~~~~~~~~~~")
    trainer = input("input your coach name please (type empty place to skip): ").strip()
    sessiontype = input("type the path of trining you want (personal,group or empty space to skip): ").strip().lower()
 
    results = gym.search(sessiontype, trainer)
 
    if len(results) == 0:
        print("there is no session under this name in our system")
        return
    print("Found", len(results), "session:")
    for s in results:
        print(s) 
 
 
def memberbookings_menu(gym):
    print("~~~~~~~~~~~~~your booked session~~~~~~~~~~~~~~~~~~~~")
    memberID = input("input your number ID: ")
 
    if memberID not in gym.members:
        print("this member is:")
        return
 
    member = find_member(gym.members, memberID)
    print( member.name, member.fname, "have in system", len(member), "booking session")
    for s in member.bookings:
        print(s)
  
 
print("WELLCOME TO GYM FITZONE ENJOY YOUR JOURNEY TO NEW LIFESTYLE")
print("get your menu to serff freally on our system , the gym is empty in this second ")
print("BOOK A SESSION NOW!!")
coaches = {
    "C20261": {"name": "remma chelfini", "classes": "pilates, cardio (HIIT)"},
    "C20262": {"name": "kamel elawaber", "classes": "MMA, booking"},
    "C20263": {"name": "bouchra smaai", "classes": "yoga, zumba"},
    "C20264":{"name": "karim elbalouchi", "classes": "teniis, soccer"}
}
gym = Gym()
member1=gym.loginnewclient("houda","aityahiha",24)
member2=gym.loginnewclient("hayat","mazanar",66)
member3=gym.loginnewclient("islam","hachad",14)
member4=gym.loginnewclient("ahmed","bouachri",52)
member5=gym.loginnewclient("sara","amine",20)
member6=gym.loginnewclient("yanis rayane","khaledi",23)
member7=gym.loginnewclient("lina farah","hamidi",31)
member8=gym.loginnewclient("nour","daoud",18)
member9=gym.loginnewclient("karim","messaoudi",27)

s1 = Groupclass(Utils.generateId(), "Yoga", "morning",
                "C20263 - bouchra smaai", 3900)
 
s2 = Groupclass(Utils.generateId(), "Pilates", "afternoon",
                "C20261 - remma chelfini", 2550)
 
s3 = Groupclass(Utils.generateId(), "MMA", "morning",
                "C20262 - kamel elawaber", 3500)
 
s4 = Personaltraining(
    "Personal Cardio",
    "morning",
    "C20261 - remma chelfini",
    Utils.generateId(),
    4560
)
 
s5 = Personaltraining(
    "Personal Boxing",
    "afternoon",
    "C20262 - kamel elawaber",
    Utils.generateId(),
    6900
)
 
s6 = Groupclass(Utils.generateId(), "Zumba", "afternoon",
                "C20263 - bouchra smaai", 2800)
 
gym.addsession(s1)
gym.addsession(s2)
gym.addsession(s3)
gym.addsession(s4)
gym.addsession(s5)
gym.addsession(s6)
gym.book_session(member1.memberID, s1.sessionID)
gym.book_session(member2.memberID, s1.sessionID)
gym.book_session(member3.memberID, s1.sessionID)
gym.book_session(member4.memberID, s1.sessionID)
gym.book_session(member5.memberID, s1.sessionID)
gym.book_session(member6.memberID, s1.sessionID)
gym.book_session(member7.memberID, s1.sessionID)
gym.book_session(member8.memberID, s1.sessionID)
gym.book_session(member9.memberID, s1.sessionID)
gym.book_session(member1.memberID, s2.sessionID)
gym.book_session(member2.memberID, s4.sessionID)

while True:
    gymmenu()
    choice = input("choose the  option you want excess to: ")
 
    try:
        if choice == "1":
            newmembership_menu(gym)
        elif choice == "2":
            addsession_menu(gym)
        elif choice == "3":
            booksession_menu(gym)
        elif choice == "4":
            cancelbooking_menu(gym)
        elif choice == "5":
            price_menu(gym)
        elif choice == "6":
            search_menu(gym)
        elif choice == "7":
            memberbookings_menu(gym)
        elif choice == "8":
            gym.statistics()
        elif choice == "9":
            gym.monthly_report()
        elif choice == "10":
            print("Wellcome again in our gym  thank you for being part of FITZONE FAMILLEY , SEE YOU AROUND MATE!! ")
            break
        else:
            print("tis is anvalid option please pick a number from the menu")
    except Exception as error:
      print("Oops there is an error go back pls to the menu!!")