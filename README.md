# HealthTrack — Clinic Management System

A Python-based clinic management system designed to handle patient 
registration, doctor assignment, medical records, and report generation 
for small to mid-size healthcare facilities.

Built as a learning project covering core Python concepts including OOP, 
Iterators, Generators, Decorators, and Context Managers.

---

## Problem It Solves

Manual clinic workflows are error-prone and slow. HealthTrack centralises 
patient data, automates prioritisation, and generates structured reports — 
reducing administrative overhead for clinic staff.

---

## Features

- **Patient Management** — registration with automatic BMI calculation and risk classification
- **Emergency Prioritisation** — patients sorted by urgency level automatically
- **Doctor Assignment** — match patients to available physicians by specialty
- **Medical Records** — medication tracking and visit history per patient
- **Report Generation** — structured summaries via Python Generators
- **Data Validation** — input sanitisation enforced through Decorators
- **Safe Transactions** — file operations wrapped in Context Managers
- **JSON Storage** — persistent local storage without a database dependency

---

## Tech Stack

| Layer        | Technology                              |
|--------------|-----------------------------------------|
| Language     | Python 3.12                             |
| Paradigm     | OOP — Inheritance, Magic Methods, Properties |
| Patterns     | Iterator, Generator, Decorator, Context Manager |
| Storage      | JSON (file-based)                       |

---

## Project Structure
```
healthtrack/
├── models.py       # Patient, Doctor domain models
├── manager.py      # Clinic business logic
├── utils.py        # Decorators, validators
└── main.py         # Entry point
```
---

## How to Run

```bash
git clone https://github.com/volkancelebidev/healthtrack.git
cd healthtrack
python main.py
```

---

## What I Learned

This project was built to practice and consolidate:
- Designing class hierarchies with inheritance and magic methods
- Implementing the Iterator and Generator protocols from scratch
- Applying Decorators for reusable input validation
- Managing file I/O safely with Context Managers
