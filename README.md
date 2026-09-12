<div align="center">

  # 📚 Smart Campus Library Management & Transaction System

  **A modular, terminal-based library automation suite featuring multi-role access control, dynamic transaction tracking, reservation queuing, and automated overdue fine calculations.**

  [![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](#)
  [![Interface](https://img.shields.io/badge/UI-Command%20Line%20Interface%20(CLI)-lightgrey?style=flat-square)](#)
  [![Persistence](https://img.shields.io/badge/Storage-JSON%20File%20I%2FO-blue?style=flat-square)](#)
  [![Coursework](https://img.shields.io/badge/UTAR-FHCT1024%20Foundations-blueviolet?style=flat-square)](#)

</div>

---

## 📌 Overview

Developed for the **FHCT1024 Programming Concepts and Design** foundational coursework at **Universiti Tunku Abdul Rahman (UTAR)**, this application simulates an institutional library management workflow through a clean, menu-driven command-line interface.

The system handles end-to-end book life cycles—from cataloging and search indexing to role-based checkout allowances, book reservation waitlists, and fine adjustments upon return.

---

## ✨ Key System Features

* 🔐 **Role-Based Access Control (RBAC)**:
  * Automatically provisions user privileges and loan limits based on verified institutional email domains (`@1utar.my` for Students, `@utar.edu.my` for Staff, `@utar.admin.my` for Administrators).
  * Enforces tailored borrowing constraints:
    * **Students**: Maximum 3 books · 7-day loan window.
    * **Staff / Administrators**: Maximum 10 books · 30-day loan window.
* 📖 **Catalog & Inventory Engineering**:
  * Complete CRUD capability for administrators (Title, Author, Category, Publisher, Publication Year, Shelf Location, and Status).
  * Multi-attribute query engine indexing by Title, Author, Category (Fiction / Non-fiction), and Year.
* 🔄 **Transaction & Reservation Pipeline**:
  * **Borrowing & Lending Flow**: Dynamic due date calculation using Python's `datetime` module.
  * **Waitlist Reservation**: Allows patrons to place reservation holds on actively borrowed items, preventing unauthorized checkouts upon check-in.
* 💰 **Overdue Fine & Return Auditor**:
  * Identifies delinquent accounts with automated overdue calculations ($RM5.00 / day overdue rate$).
  * Supports transactional settlement with payment change computation.
* 💾 **File Persistence**:
  * Employs formatted JSON files (`books.txt`, `users.txt`, `borrowedlibrary_data.txt`, `reservedlibrary_data.txt`) to reliably persist records across sessions.

---

## 🏗️ Architecture & Storage Models

```text
├── P2_G3_FHCT1024_2410.py    # Main program entry & controller routines
├── books.txt                 # Master book inventory catalogue (JSON)
├── users.txt                 # User registry credentials & role mappings (JSON)
├── borrowedlibrary_data.txt  # Active loan transactions & timestamp logs (JSON)
├── reservedlibrary_data.txt  # Queued book holds & reservations (JSON)
└── README.md
