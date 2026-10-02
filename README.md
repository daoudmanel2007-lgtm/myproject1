# 🏋️ FitZone — Gym Management System

**FitZone** is an interactive console application for managing a gym, developed as a student project in Computer Science.
It is fully coded in **Python** using object-oriented programming, with no external libraries required.

## 🎮 Overview

FitZone lets a gym manage its members and sessions from a simple text menu.
You can register members, create group or personal training sessions, book and cancel them, calculate prices with discounts, and follow the gym's activity through statistics and reports.

## ✨ Features

- 🪪 **New membership**: register a member and get a unique ID (e.g. `FTZALG20261`)
- ➕ **Add a session**: choose name, period (morning/afternoon), coach, and type (group or personal)
- 📅 **Book a session**: with capacity checks and an automatic waiting list for group classes
- ❌ **Cancel a booking**: the first person on the waiting list is promoted automatically
- 💰 **Price calculation**: includes the first-time card fee and age discounts
- 🔍 **Search**: filter sessions by coach and/or session type
- 👤 **Member bookings**: display all sessions booked by a member
- 📊 **Statistics**: totals, most popular session, and a popularity ranking
- 🧾 **Monthly report**: per-member summary with final prices

## 💰 Pricing Rules

| Rule | Effect |
|------|--------|
| First-time member | +500 DA card fee (charged once) |
| Age under 18 or 60 and over | 15% discount |
| Group class | Base cost divided by the number of participants |
| Personal training | Fixed hourly rate |

## 🏃 Session Types

| Type | Capacity | Waiting list | Price |
|------|----------|--------------|-------|
| 👥 Group class | 8 | ✅ Yes | `base cost / participants` |
| 🧍 Personal training | 1 | ❌ No | `hourly rate` |

## 🧠 Technologies & Concepts

- 🐍 **Python 3** (standard library only)
- 🧱 **Abstraction**: `ABC` and `@abstractmethod`
- 🧬 **Inheritance & polymorphism**: `calculate_price()` and `maxcapacity()` differ per session type
- 🔒 **Encapsulation**: logic organized in the `Utils`, `Session`, `Member`, and `Gym` classes
- ✨ **Magic methods**: `__str__`, `__eq__`, `__len__`
- 🛡️ **Exception handling**: `try / except` for input validation

## 🗂️ Project Structure

| Component | Role |
|-----------|------|
| `Utils` | ID generation and price/discount calculation |
| `Session` (abstract) | Base class for all sessions |
| `Groupclass` | Group session with a waiting list |
| `Personaltraining` | One-to-one session |
| `Member` | Member data, booking and cancelling logic |
| `Gym` | Main manager: members, sessions, search, statistics, reports |
| `*_menu()` functions | Console interface for each menu option |

## 🚀 Installation & Launch

### 1️⃣ Prerequisites

Make sure **Python 3.8 or higher** is installed on your machine.
No extra libraries are needed.

### 2️⃣ Clone the project

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 3️⃣ Run the program

```bash
python main.py
```

Replace `main.py` with the name of your file.

### 4️⃣ Use the menu 🎉

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     THE MENU of the gym FitZone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1.new membership
2.add a new session
3.book a session
4.cancel a booking
5.calculate the price of the session
6.search for a session
7.display a member's booked session
8.display overall statistics
9.automatic monthly report
10.EXIT cleanly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

Type the number of the option you want and follow the prompts.

## 🧪 Demo Data

The program starts with sample data so you can test it right away:

- 👥 **9 members** (ages from 14 to 66)
- 🏋️ **6 sessions**: Yoga, Pilates, MMA, Zumba (group) and Personal Cardio, Personal Boxing (personal)
-
