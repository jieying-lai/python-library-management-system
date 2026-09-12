import datetime
import json

booklist = "books.txt"
userslist = "users.txt"
dd={}

def load_book_info(): 
    try:
        with open(booklist, "r") as file:
            dd = json.load(file)
            return dd
    except FileNotFoundError:
        print(f"File {booklist} not found. Starting with an empty book list.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {booklist} contains invalid JSON.")
        return {}

def load_user_info(): 
    try:
        with open(userslist, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("User file not found. Starting with an empty user list.")
        return {}
    except json.JSONDecodeError:
        print("Error: The user file contains invalid JSON.")
        return {}

def save_user_info(users): 
    try:
        with open(userslist, "w") as file:
            json.dump(users, file, indent=4)
        print("Data saved successfully.")
        
    except Exception as e:
        print("There is an error in saving data")


users = load_user_info()


def validated_email_and_role(): 
    repeat = True
    while repeat:
        email = input("Enter your email: ").lower()
        
        if "@" not in email:
            print("Invalid email. An email must contain '@'. Please try again.")
            
        elif not email.endswith("1utar.my") and not email.endswith("utar.edu.my") and not email.endswith("utar.admin.my"):
            print("Invalid email. Please use a valid UTAR email domain.")
            
        else:
            
            if email.endswith("@1utar.my"):
                role = "Student"
                repeat=False
                
            elif email.endswith("@utar.edu.my"):
                role = "Staff"
                repeat=False
                
            elif email.endswith("@utar.admin.my"):
                role = "Administrator"
                repeat=False
            else:
                print("Unknown email domain. Please try again.")
                
            return email, role

def search_user(email_login): 
    users = load_user_info()

    repeat = True
    while repeat:
        
        print("-"*50)
        print("\t-----Search User System-----")
        print()
        
        print("Search by:")
        print("\t<I>d")
        print("\t<N>ame")
        print("\t<E>mail")
        print()
        print("\t<R>eturn")

        keymap={
            "I":"id",
            "N":"name",
            "E":"email",

            }

        answer = input("Enter your choice \n>> ").upper()

        if answer == "R":
            print("Return to previous menu...")
            repeat = False
            continue
            
        elif answer not in keymap:
            print ("Invalid choice. Please try again.")
            continue


        searchkey   = keymap[answer]

        info        = input("Enter %s to search >> "%searchkey).strip().lower()        
       
        found_users = []
        
        for email, user_info in users.items():
            if searchkey == "email" and info in email.lower():
                found_users.append({"email":email, **user_info})

            elif searchkey != "email" and info in user_info.get(searchkey, "").lower():
                found_users.append({"email":email, **user_info})
                
        if found_users:
            print("-" * 50)
            print("Search Results:\n")
            for user in found_users: 
                print(" ID: %s \n Name: %s \n Email: %s \n Role: %s" % (user['id'], user['name'], user['email'], user['role']))
                print("-" * 50)

        else:
            print("-" * 50)
            print("No users found with %s: %s"%(searchkey,info))
            print("-" * 50)
            
        selection = input("Do you want to search again? (Y/N): ").upper()
        
        if selection != "Y":
            print("-" * 50)
            print("Returning to previous menu...")
            repeat = False

def validated_password(): 
    repeat = True
    while repeat:
        password = input("Enter your password: ")
        
        if len(password) < 8:
            print("Invalid password. Password should be at least 8 characters.")
        
        else:
            confirm_password = input("Confirm your password: ")
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                
            else:
                print("Password successfully set!")
                return password
                repeat = False

def is_profile_id_taken(profile_id, users):
    return any(user["id"] == profile_id for user in users.values())

def register_user_info(users):
    
    users = load_user_info()
    print()
    print("\t        XXLibrary System")
    print("\t------- User Registration -------")
    
    profile_id = input("Enter new ID \n(or type 'return' to exit): ").strip()

    if profile_id.upper() == "RETURN":
        return users

    if not profile_id:
        print("ID cannot be empty.\n")
        return users
    
    if is_profile_id_taken(profile_id, users):
        print("ID already registered. Please try logging in.\n")
        return users
    
    name = input("Enter the name: ").strip().upper()
    if not name:
        print("Name cannot be empty. ")
        return users
    
    email, role = validated_email_and_role()
    
    if email in users:
        print("Email already registered. Please try logging in.\n")
        return users
    

    password = validated_password()

    users[email] = {"id":profile_id,
                    "name": name,
                    "password": password,
                    "role": role,
                }
    
    save_user_info(users)
    print(f"Registration successful! Welcome, {name}. Your role is {role}.\n")
    return users


def login_user(): 
    users = load_user_info()
    print("\n\t--------- Login Menu ---------\n")
    repeat= True
    while repeat:
         email_login = input("Enter your email (or type 'return' to quit)\n>> ").lower()
         
         if email_login == "return":
            print("Exiting login process.")
            repeat = False
        
         else:
            password_login = input("Enter your password\n>> ")

            if email_login in users and users[email_login]["password"] == password_login:
                repeat = False
                print(f"Login successful! Welcome back, {users[email_login]['name']} ({users[email_login]['role']}).\n")
                user_view(email_login)
                
                return

            else:
                print("Invalid email or password. Please try again.\n")

    
def update_user_profile(email_login): 
    
    users = load_user_info()
    role = users[email_login]['role']
    
    if email_login not in users:
        print("Invalid user session. Please log in again.")
        return
    
    user = users[email_login]

    print("-"*49)
    print("\t       User Profile Management")
    print("\t         Update Profile Data")
    print("\t-------- %-12s View ---------" %role)
  
    print("\nEnter new details or press ENTER to keep current values:")

    new_name = input(f"Current name: {user['name']} \nNew name >> ").strip().upper()

    if new_name:
        users[email_login]["name"] = new_name

    repeat = True
    while repeat:
        new_password = input(f"Current password: {user['password']} \nNew password >> ").strip()

        if new_password:
            if len(new_password) < 8:
                print("Password must be at least 8 characters.")
            else:
                users[email_login]["password"] = new_password
                repeat = False
        else:
            repeat = False
    
    save_user_info(users)
    
    if new_name or new_password:
        print("Profile updated successfully.")
    else:
        print("No changes were made.")


def delete_profile(): 
    users=load_user_info()
    print("\t-----Deletion of User-----")
    print("\t------- Admin View -------")
    print()
    profile_id=input("Enter ID to delete\n>> ")
    
    found_email = None
    
    for email, info in users.items():
        if info['id'] == profile_id:
            found_email = email
            break

    if not found_email:
        print("-" * 50)
        print("ID not found.")
        return
    
    else:
        confirm = input("Are you sure you want to delete this account? (<Y>es/<N>o): ").upper()

        if confirm == "Y":
            del users[found_email]

            save_user_info(users)
            
            print("-"*50)
            print("Account deleted successfully!")
        
        else:
            print("-"*50)
            print("Deletion canceled.")

def total_users(): 
    
    users = load_user_info()
    print("Total user list:")
    print("-"*70)
    print(" ID         | Name       | Email                     | Role")
    print("-"*70)

    for email,users in users.items():
         print(" %-10s | %-10s | %-25s | %-15s" % (users['id'], users['name'], email, users['role']))
    print("-" * 70)
        
def sync_record(email_login): 
    users = load_user_info()
    repeat = True
    while repeat:
        print("-"*50)
        print("\t     Sync User Record")
        print("\t------- Admin View -------" )
        print()
    
        print("\t<S>earch User")
        print("\t<T>otal User")
        print("\n\t<R>eturn")

        selection = input("Enter your selection\n>> ").upper().strip()
        if selection == "S":
            search_user(email_login)

        elif selection == "T":
            print()
            total_users()
            print("Total users: %d"%len(users))
            repeat = False
            
        elif selection == "R":
            print("-"*50)
            print("Returning to previous menu... ")
            repeat = False

        else:
            print("Invalid selection.Please try again.")
    
    
def edit_profile(email_login): 
    repeat = True
    while repeat:
        print("-"*49)
        print("\t    User Profile Management ")
        print("\t--------- Admin View ---------")
        
        print("-"*49)
        print("\t<A>dd     User")
        print("\t<U>pdate  Profile Data")
        print("\t<D>elete  User")
        print("\t<S>ync    User Record")
        print("\n\t<R>eturn")
        profile=input(">> ").upper()
        if profile =="A":
            register_user_info(users)
            
        elif profile == "U":
            update_user_profile(email_login)
           
        elif profile =="D":
            delete_profile()
            
        elif profile == "S":
            sync_record(email_login)
            
        elif profile == "R":
            print("-"*50)
            print("Returning to previous menu...")
            repeat=False
                
        else:
            print("Invalid option. Please try again.")
        
def get_bookid(dd): 
    repeat = True
    while repeat:
        bookid = input("Enter book ID (or type 'return'to exit)\n>> ")
        
        if bookid in dd:
            print("-"*50)
            print("Book ID already exists. Please use a unique ID.")
        else:
            return bookid
            repeat = False

def get_category(): 
    repeat = True
    while repeat:
        category = input("Enter book category: \n<F>iction\n<N>on-fiction\n>> ").upper()
        
        if category == "F":
            return "Fiction"
            repeat = False
        elif category == "N":
            return "Non-fiction"
            repeat = False
        else:
            print("-"*50)
            print("Invalid book category. Please try again.")

def get_year(): 
    repeat = True
    while repeat:
        try:
            year = int(input("Enter year of publication\n>> "))
            return year
            repeat = False
        except ValueError:
            print("-"*50)
            print("Invalid year format. Please enter a valid year.")

def get_status():
    repeat = True
    while repeat:
        status=input("<A>vailable\t<B>orrowed\t<M>aintenance\n>> ").upper()

        if status == "A":
            return "Available"
            repeat = False
            
        elif status == "B":
            return "Borrowed"
            repeat = False
            
        elif status =="M":
            return "Under Maintenance"
            repeat = False
            
        else:
            print("-"*50)
            print("Invalid status. Please try again.")
        
def add_books(dd,booklist):
    
    dd=load_book_info()
    
    print("-"*50)
    
    bookid    = get_bookid(dd)
    
    if bookid.upper() == "RETURN":
        return
            
    title     = input("Enter book title\n>> ").upper()
    author    = input("Enter book author\n>> ").upper()
    
    category  = get_category()
    
    publisher = input("Enter book publisher\n>> ").upper()

    year      = get_year()

    location  = input("Enter the location of the book (e.g., alphabet of shelf)\n>> ").upper()

    status    = get_status()
    
    dd[bookid]= {
        "title": title,
        "author": author,
        "category": category,
        "publisher": publisher,
        "year": year,
        "location": location,
        "status":status
    }

    try:
        with open(booklist, "w") as file:
            json.dump(dd, file, indent=4)
        print("-"*50)
        print("Book added successfully!")
    except Exception as e:
        print(f"Error saving the book list: {e}")

    return dd

def edit_book(dd,booklist): 
    dd=load_book_info()
    bookid = input("Enter book ID to edit\n>> ")
    
    if bookid not in dd:
        print("-"*50)
        print("Book ID not found.")
        return 
    
    print("-"*50)
    print("Book found!")
    print("Enter new details or press ENTER to keep current values:")
    print()
    title = input("Current title: %s \nNew title >> " %dd[bookid]['title']).upper().strip()
    if title:
        dd[bookid]['title'] = title

    print()
    author = input("Current author: %s \nNew author >> " %dd[bookid]['author']).upper().strip()
    if author:
        dd[bookid]['author'] = author
    print()
    loop = True
    
    while loop:    
        category = input("Current category: %s \nNew category <F>iction/<N>on-fiction) >> " %dd[bookid]['category']).upper().strip()
    
        if category:
            if category == "F":
                dd[bookid]['category'] = "Fiction"
                loop = False
            elif category == "N":
                dd[bookid]['category'] = "Non-fiction"
                loop = False
            else:
                print("-"*50)
                print("Invalid category! Please enter <F> for Fiction or <N> for Non-fiction.")
                
        else:
            loop = False
    print()
    publisher = input("Current publisher: %s \nNew publisher >> "%dd[bookid]['publisher']).upper().strip()
    if publisher: 
        dd[bookid]['publisher'] = publisher
    print()

    loop = True
    while loop:
        year = input("Current year     : %s \nNew year >> "%dd[bookid]['year']).strip()
    
        if year:
            if year.isdigit():
                dd[bookid]['year'] = int(year)
                loop = False
            else:
                print("-"*50)
                print("Invalid year format! Please enter a valid year.")
        else:
            loop = False
    print()   
    location = input("Current location : %s \nNew location >> " %dd[bookid]['location']).upper().strip()
    
    if location: 
        dd[bookid]['location'] = location

    print()
    loop = True
    while loop:
        status    = input("Current status   : %s \nNew status \n<A>vailable\n<B>orrowed\n<M>aintenance\n>> " %dd[bookid]['status']).upper().strip()
        if status:
            if status == "A":
                dd[bookid]['status'] = "Available"
                loop = False
            elif status == "B":
                dd[bookid]['status'] = "Borrowed"
                loop = False
            elif status == "M":
                dd[bookid]['status'] = "Under Maintenance"
                loop = False
            else:
                print("-"*50)
                print("Invalid status! Please enter <A> for Available, <B> for Borrowed, or <M> for Maintenance.")
                
        else:
            loop = False

    with open(booklist, "w") as file:
        json.dump(dd, file, indent=4)
        
    print("-"*50)
    print("Book details updated successfully!")
    return 

def delete_book(dd,booklist):
    dd=load_book_info()

    bookid = input("Enter book ID to delete\n>> ")
    if bookid not in dd:
        print("-"*50)
        print("Book ID not found.")
        return 

    confirm = input("Are you sure you want to delete book <%s> ? (<Y>es/<N>o): " %dd[bookid]['title']).upper()
    
    if confirm == "Y":
        del dd[bookid]
        with open(booklist, "w") as file:
            json.dump(dd, file, indent=4)
        print("-"*50)
        print("Book deleted successfully!")
    else:
        print("-"*50)
        print("Deletion canceled.")
    
    return 

def search_book(dd, booklist):
    
    dd=load_book_info()
    repeat = True
    
    while repeat:
        print("-"*50)
        print("Welcome to search system :)")
        print("Search by: ")
        print("<T>itle of book")
        print("<A>uthor of book")
        print("<C>ategory of book")
        print("<Y>ear of publishcation")
        print()
        print("<R>eturn")
        key_map = {
            "T": "title",
            "A": "author",
            "C": "category",
            "Y": "year",

            }

        choice = input("Enter your choice \n>> ").upper()
        
        if choice == "R":
            print("-" * 50)
            print("Returning to previous menu...")
            repeat = False
            
            
        elif choice not in key_map:
            print("Invalid choice. Please try again.")
            
        else:
            search_key = key_map[choice]
            
            if search_key == "category":
                detail = input ("Which category you want to search \n<F>iction\n<N>on-fiction\n >> ").upper().strip()
                if detail == "F":
                    detail = "Fiction"
                    
                elif detail == "N":
                    detail = "Non-fiction"
                    
                else:
                    print("Invalid selection. Please try again")
                    continue
                
            else:

                detail = input("Enter which %s do you want to search\n >> "%search_key).upper().strip()
                print()
                
            found_books = []
        
    
            for bookid, book in dd.items():
                if detail.upper() == str(book.get(search_key, "")).upper():
                    found_books.append((bookid, book))

            if not found_books:
                print("Sorry this book is not available:( Please try again...")

            else:
                print("------Your book is found! Please check it out~ ------\n")

                print("%-10s | %-25s | %-20s | %-20s | %-20s | %-10s | %-15s | %-10s"
                      % ("Book ID", "Title", "Author", "Category", "Publisher", "Year", "Location", "Status"))
                print("-"*150)

               
                for bookid, found_book in found_books:
                    print("%-10s | %-25s | %-20s | %-20s | %-20s | %-10s | %-15s | %-10s"
                          % (bookid,
                            found_book['title'],
                            found_book['author'],
                            found_book['category'],
                            found_book['publisher'],
                            found_book['year'],
                            found_book['location'],
                            found_book['status']
                        ))
                print("-"*150)

                repeat = input("Do you want to search again? (Y/N): ").upper()

                if repeat != "Y":
                    print("-" * 50)
                    print("Returning to previous menu...")
                    repeat = False
                
def book_info_list(): 
    
    dd=load_book_info()
    
    if dd is None:  
        print("Error loading book data. Please check the book file.")
        return
    
    print("-"*50)
    print("Book Info List: \n")
    print("\t<A>vailable")
    print("\t<B>orrowed ")
    print("\t<U>nder Maintenance")
    print("\t<T>otal")
    print()
    print("or type 'return' to quit")
    
    action = input("\n>> ").upper()
    
    if action == "RETURN":
        print("-" * 50)
        print("Returning to previous menu....")
        return
        
    elif action == "A":
        available_books=[]
        
        print("-"*50)
        print("Available Books:")
        print("Book ID \t Book title")
        print("-"*50)
        
        for bookid, book in dd.items():
            if book['status'] == "Available":
                
                available_books.append(book['title'])
                print("%s \t\t %-20s"   %(bookid,book['title']))

        print("-"*50)
        print("Total number of avalable books: %02d"   %len(available_books))
        print()
        
    elif action =="B":
        borrowed_books=[]
        
        print("-"*50)
        print("Borrowed Books:")
        print("Book ID \t Book Title \t\t Borrowed By")
        print("-"*50)

        try:
            with open("borrowedlibrary_data.txt", "r") as f:
                borrowed_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            borrowed_data = []
        
        
        for bookid, book in dd.items():
            if book['status'] == "Borrowed":
                borrower_entry = next(
                    (entry for entry in borrowed_data if entry['b_id'].strip() == bookid.strip()), None
                    )
                borrower = borrower_entry['b_user'] if borrower_entry else "Unknown"
                borrowed_books.append(book['title'])
                print("%s \t\t %-20s \t %-20s"   %(bookid,book['title'],borrower))

        print("-"*50)
        print("Total number of borrowed books:%02d"   %len(borrowed_books))
        print()

    elif action =="U":
        main_books=[]
        
        print("-"*50)
        print("Under Maintenance Books:")
        print("Book ID \t Book title")
        print("-"*50)
        
        for bookid, book in dd.items():
            if book['status'] == "Under Maintenance":
                
                main_books.append(book['title'])
                print("%s \t\t %-20s"   %(bookid,book['title']))

        print("-"*50)
        print("Total number of under maintenance books: %02d"   %len(main_books))
        print()

    elif action == "T":  
    
        print("-"*70)
        print("Total Books: ")
        print("Book ID \t Book title \t\t Status")
        print("-"*70)
        total_book=[]
        
        for bookid, book in dd.items():
            total_book.append(book)
            print("%s \t\t %-20s \t %s"   %(bookid,book['title'],book['status']))
            
        print("-"*70)
        print("Total number of books: %02d"   %len(total_book))
        print()

    else:
        print("-"*50)
        print("Invalid selection!")
     
def handle_borrowing(bookid, book, dd, users, email_login, loan_period, borrowed_data):

    choice = input("Do you want to borrow the book? <Y>es or <N>o \n>> ").strip().upper()
    
    if choice == "Y":
        status = "Borrowed"
        dd[bookid]['status'] = status

        borrow_date = datetime.date.today()
    
        due_date = borrow_date + datetime.timedelta(days = loan_period)

        b_data ={
            'b_id': bookid,          
            'b_bookname': dd[bookid]['title'],  
            'b_userid': users[email_login]['id'],  
            'b_user': users[email_login]['name'],  
            'borrow_date': str(borrow_date),       
            'due_date': str(due_date),             
            }
        
        borrowed_data.append(b_data)
        save_to_file("borrowedlibrary_data.txt", borrowed_data)
        print("Book successfully borrowed!")
    
    else:
         print("You chose not to borrow the book.")

def handle_reservation(bookid, book, dd, users, email_login): 

    try:
        with open('borrowedlibrary_data.txt', 'r') as f:
            borrowed_data = json.load(f)
    except FileNotFoundError:
        borrowed_data = []
    
    user_already_borrowed = any(
        entry['b_id'] == bookid and entry['b_userid'] == users[email_login]['id']
        for entry in borrowed_data
    )

    if user_already_borrowed:
        print("You have already borrowed this book.")
        return
    
    choice = input("Do you want to reserve the book? <Y>es or <N>o \n>> ").strip().upper()

    if choice == "Y":
        
        reservation_date = datetime.date.today()
        
        try:
            with open('reservedlibrary_data.txt', 'r') as f:
                existing_reservations = json.load(f)
        except FileNotFoundError:
            existing_reservations = []

        user_already_reserved = any(res['r_id'] == bookid and res['r_userid'] == users[email_login]['id']for res in existing_reservations)

        if user_already_reserved:
            print("You have already reserved this book.")
            return

        r_data ={
            'r_id': bookid,
            'r_bookname': dd[bookid]['title'],
            'r_userid': users[email_login]['id'],
            'r_user': users[email_login]['name'],
            'reservation_date': str(reservation_date),
         }
                    
                    
        existing_reservations.append(r_data)
        save_to_file('reservedlibrary_data.txt', existing_reservations)
        print("Book successfully reserved!")
    else:
        print("You chose not to reserve the book.")


def save_to_file(filename, data): 
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

            
def display_borrowed_books(email_login,users, borrowed_data):
    
    try:
        with open('borrowedlibrary_data.txt', 'r') as f:
            borrowed_data = json.load(f)
    except FileNotFoundError:
        borrowed_data = []
        
    user_id = users[email_login]['id']
    b_borrow = [entry for entry in borrowed_data if entry['b_userid'] == user_id]
    
    print("\nBorrowed Books Info:")
    print("-" * 80)
    print("%-10s | %-25s | %-15s | %-15s " % ("Book ID", "Title", "Borrow Date", "Due Date"))
    print("-" * 80)


    for entry in b_borrow:
        print("%-10s | %-25s | %-15s | %-15s " % (
            entry['b_id'], 
            entry['b_bookname'], 
            entry['borrow_date'], 
            entry['due_date']
        ))

    print("-"*80)
    print()
    print("Number of borrowed books: %2d" %len(b_borrow))
    print("\nBook details updated successfully!") 

    
def display_reserved_books(existing_reservations): 

    try:
        with open('reservedlibrary_data.txt', 'r') as f:
            existing_reservations = json.load(f)
    except FileNotFoundError:
            existing_reservations = []
    
    print("\nReserved Books Info:")
    print("-" * 95)
    print("%-10s | %-25s | %-15s | %-15s | %-15s" % ("Book ID", "Title", "User ID","User","Reservation Date"))
    print("-" * 95)


    for entry in existing_reservations:
        print("%-10s | %-25s | %-15s | %-15s | %-15s" % (
            entry['r_id'], 
            entry['r_bookname'],
            entry['r_userid'],
            entry['r_user'], 
            entry['reservation_date']
        ))

    print("-" * 95)
    print()
    print("Number of reservation: %2d" %len(existing_reservations))

def borrow_book (email_login): 
    
    users = load_user_info()
    dd = load_book_info()
    role = users[email_login]['role'].lower()

    if role == "student":
        view = "User"
        borrow_limit = 3
        loan_period = 7
        
    elif role == "staff":
        borrow_limit = 10
        view = "User"
        loan_period = 30
        
    else:
        borrow_limit = 10
        view = "Admin"
        loan_period = 30

    print("-"*50)
    print("\t    Borrow Book Menu")
    print("\t------- %s View -------" %view)
    
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M")
    print(date_time_str)
    
    try:
        with open('borrowedlibrary_data.txt', 'r') as f:
            borrowed_data = json.load(f)
        if not isinstance(borrowed_data, list):
            raise ValueError("Invalid data format in borrowedlibrary_data.txt")
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        borrowed_data = []

    user_id = users[email_login]['id']
    borrowlist = [entry for entry in borrowed_data if entry.get('b_userid') == user_id]
    borrowed_books_count = len(borrowlist)

    if borrowed_books_count >= borrow_limit:
        print(f"You have reached your borrowing limit of {borrow_limit} books.")
        return

    repeat = True
    while repeat:
        
        print("-"*50)
        print("Total borrowed books: %2d / %2d" %(borrowed_books_count, borrow_limit))
        print()
        print("Do you want to search book ID to borrow book?\n")
        print("(or type 'return' to quit)")
        search = input("\n<Y>es or <N>o \n>>").strip().upper()

        if search == 'RETURN':
            print("-" * 50)
            print("Returning to previous menu...")
            repeat = False
        
        elif search == "Y":
            search_book(dd,booklist)

        elif search == "N":
            bookid = input("Enter book ID to borrow\n>> ").strip()
            
            if bookid not in dd:
                print("-"*50)
                print("Book ID not found.")
                return 
            
            print("-"*50)
            
            book = dd[bookid]
            print("Book found! <%s>"%book['title'])
            print("Current status: %s"%book['status'])

            if book['status'] == "Available":

                try:
                    with open('reservedlibrary_data.txt', 'r') as f:
                        reserved_books = json.load(f)
                except FileNotFoundError:
                    reserved_books = []

                reservation = next((res for res in reserved_books if res['r_id'] == bookid), None)

                if reservation:
                    if reservation['r_userid'] == users[email_login]['id']:
                        handle_borrowing(bookid, book, dd, users, email_login, loan_period, borrowed_data)

                        reserved_books = [res for res in reserved_books if res['r_id'] != bookid]
                        save_to_file('reservedlibrary_data.txt', reserved_books)
                        print("Your reservation has been removed after borrowing the book.")
                        repeat = False

                    else:
                        print("This book is reserved by another user. You cannot borrow it.")
                        repeat = False
                else:
                    
                    handle_borrowing(bookid, book, dd, users, email_login, loan_period, borrowed_data)
                    repeat = False
                    

            elif book['status'] == "Borrowed":
                handle_reservation(bookid, book, dd, users, email_login)
                repeat = False

            else:
                print("This book is not available for now.")

            try:
                with open(booklist, "w") as file:
                    json.dump(dd, file, indent=4)
            except Exception as e:
                print(f"Error saving the book list: {e}")

            display_borrowed_books(email_login,users,borrowed_data)
            
        else:
            print("Invalid input. Please try again.")



def return_book (email_login): 
    from datetime import datetime
    users = load_user_info()
    dd = load_book_info()

    role = users[email_login]['role'].lower()

    if role == "student":
        view = "User"
        borrow_limit = 3
        loan_period = 7
        
    elif role == "staff":
        borrow_limit = 10
        view = "User"
        loan_period = 30
    else:
        borrow_limit = 10
        view = "Admin"
        loan_period = 30

    try:
        with open('borrowedlibrary_data.txt', 'r') as f:
            borrowed_data = json.load(f)
        if not isinstance(borrowed_data, list):
            raise ValueError("Invalid data format in borrowedlibrary_data.txt")
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        borrowed_data = []

    user_id = users[email_login]['id']
    borrowlist = [entry for entry in borrowed_data if entry.get('b_userid') == user_id]
    borrowed_books_count = len(borrowlist)

    print("-"*50)
    print("Total borrowed books: %2d / %2d" %(borrowed_books_count, borrow_limit))

    if borrowed_books_count == 0:
        print()
        print("No book is found")
        return

    else: 
        print()
        display_borrowed_books(email_login,users,borrowed_data)
        print()

        
        print("Do you want to return the book ?\n")
        
        selection = input("<Y>es or <N>o \n>> ").upper()
        
        if selection == "Y":
            book_id = input("Enter the book ID >> ")

            book_to_return = next((entry for entry in borrowlist if entry['b_id'] == book_id), None)

            
            if book_to_return:
                due_date = datetime.strptime(book_to_return['due_date'], '%Y-%m-%d').date()
                today = datetime.now().date()
                
                if due_date < today:
                    overdue_days = (today - due_date).days
                    fine = overdue_days * 5
                    print(f"Late return detected! Overdue by {overdue_days} days. Fine: ${fine}.")
                    print("Please visit the library to pay your fine.")
                    
                else:   
                    borrowed_data.remove(book_to_return)
                    
                    dd[book_id]['status'] = "Available"
            
                    try:
                        save_to_file("borrowedlibrary_data.txt", borrowed_data)

                        try:
                            with open(booklist, "w") as file:
                                json.dump(dd, file, indent=4)
                        except Exception as e:
                            print(f"Error saving the book list: {e}")
                
                        print("-" * 50)
                        print("Book with ID %s has been successfully returned."%book_id)
                    except Exception as e:
                        print(f"Error saving data: {e}")

            else:
                print(f"No book with ID {book_return} found in your borrowed books.")

        elif selection == "N":
            print("Return book process canceled.")

        else :
            print("Invalid selection. Please try again.")
        
    
        
def book_transaction(email_login): 
    
    users = load_user_info()
    dd=load_book_info()
    
    try:
        with open('borrowedlibrary_data.txt', 'r') as f:
            borrowed_data = json.load(f)
        if not isinstance(borrowed_data, list):
            raise ValueError("Invalid data format in borrowedlibrary_data.txt")
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        borrowed_data = []
        
    try:
        with open('reservedlibrary_data.txt', 'r') as f:
            existing_reservations = json.load(f)
    except FileNotFoundError:
            existing_reservations = []

    status = True
    while status:
        print("-"*50)
        print("Book Transaction Tracking:\n")
        print("\t<B>orrow Book")
        print("\t<R>eturn Book")
        print("\t<S>earch Book")
        print("\t<P>rint Borrow History")
        print("\t<L>ist of Book's Reservation")
        print()
        print("(or type 'return' to quit)")
        tran = input("\n>> ").upper()
       
        if tran == "RETURN":
            print("-" * 50)
            print("Returning to previous menu...")
            status = False
        
        elif tran == "B":
            borrow_book(email_login)
            

        elif tran == "R":
            return_book(email_login)
            

        elif tran == "S":
            search_book(dd, booklist)
            

        elif tran == "P":
            display_borrowed_books(email_login,users,borrowed_data)
            

        elif tran == "L":
            display_reserved_books(existing_reservations)
            

        else:
            print("Invalid selection. Please try again.")
              

def overdue_books(): 
    
    from datetime import datetime
    
    try:
        with open('borrowedlibrary_data.txt', 'r') as f:
            borrowed_data = json.load(f)
        if not isinstance(borrowed_data, list):
            raise ValueError("Invalid data format in borrowedlibrary_data.txt")
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        borrowed_data = []

    overdue_list = []

    today = datetime.now().date() 

    for book in borrowed_data:
        try:
            due_date = datetime.strptime(book['due_date'], '%Y-%m-%d').date()
            if due_date < today:
                overdue_days = (today - due_date).days
                fine = overdue_days * 5 
                book['overdue_days'] = overdue_days
                book['fine'] = fine
                overdue_list.append(book)
        except (KeyError, ValueError) as e:
            
            print(f"Skipped invalid entry: {book}. Error: {e}")
            continue

    return overdue_list

def adjust_overdue(): 
    from datetime import datetime
    
    try:
        with open('borrowedlibrary_data.txt', 'r') as f:
            borrowed_data = json.load(f)
        if not isinstance(borrowed_data, list):
            raise ValueError("Invalid data format in borrowedlibrary_data.txt")
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        borrowed_data = []

    dd = load_book_info()
    
    overdue = overdue_books()

    book_id = input("Enter the Book ID to adjust: ").strip()
    book_to_adjust = next((book for book in overdue if book['b_id'] == book_id), None)
    if not book_to_adjust:
        print(f"No overdue book found with ID {book_id}.")
        return

    repeat = True
    while repeat:
        try:
            paid = float(input(f"Enter the amount paid (Fine: RM {book_to_adjust['fine']}): RM ").strip())
            repeat = False
        except ValueError:
            print("Invalid input. Please enter a valid number for the amount paid.")
            
    if paid < book_to_adjust['fine']:
        print(f"Insufficient payment. RM {book_to_adjust['fine'] - paid} is still outstanding.")
        return
    
    elif paid > book_to_adjust['fine']:
        print(f"Overpayment detected. Change: RM {paid - book_to_adjust['fine']}")

    borrowed_data = [entry for entry in borrowed_data if entry['b_id'] != book_id]
    dd[book_id]['status'] = "Available"

    save_to_file("borrowedlibrary_data.txt", borrowed_data)

    try:
        with open(booklist, "w") as file:
            json.dump(dd, file, indent=4)
    except Exception as e:
        print(f"Error saving the book list: {e}")

    print(f"Book ID {book_id} returned successfully, and fine paid.")
    
def user_view(email_login): 
    users = load_user_info()
    
    role = users[email_login]['role']
    now  = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M")
    
    if role.lower() == "administrator":
        repeat = True
        while repeat:
    
            print("-"*50)
            print("\tXXLibrary System Main Menu")
            print("\t------- Admin View -------")
            print("\tAdminstrator : %s" %users[email_login]['name'])
            print("\tLogin time:",date_time_str)
            print()
            
            print("<1> User Profile Management")
            print("<2> Book Tracking & Inventory Management")
            print("<3> Book Transaction Tracking")
            print("<4> Overdue Books and Fines")
            print()
            print("<L> Log Out")
            
            menu = input("Opt >> ").strip()
            
            if menu.upper() == "L":
                print("Exiting Admin View. Goodbye!")
                repeat = False
            
            elif menu =="1":
                edit_profile(email_login)

            elif menu == "2":
                management(email_login)
                
            elif menu == "3":
                book_transaction(email_login)

            elif menu == "4":
                
                overdue = overdue_books()
                if overdue:
                    print(date_time_str)
                    print("Overdue Books:")
                    print("-" * 110)
                    print("%-10s | %-25s | %-15s | %-15s | %-15s | %-15s " % ("Book ID", "Title", "User","Borrow Date", "Due Date","Fine (RM)"))
                    print("-" * 110)
                    for book in overdue:
                        print("%-10s | %-25s | %-15s | %-15s | %-15s | %-15s " % (
                            book['b_id'], 
                            book['b_bookname'],
                            book['b_user'],
                            book['borrow_date'], 
                            book['due_date'],
                            book['fine']
                        ))
                    print("-" * 110)
                    print()
                    adjust_overdue()
                else:
                    print("No overdue books.") 
                                
            else:
                print("Invalid selection. Please try again.")
                
    else:
        repeat = True
        while repeat:
            
            print("-"*50)
            print("\tXXLibrary System Main Menu")
            print("\t------------ User View ------------")
            print("\tUser : %s" %users[email_login]['name'])
            print("\tRole: %s" %users[email_login]['role'])
            print("\tLogin time:",date_time_str)
            print()
            
            print("<1> User Profile Management")
            print("<2> Book Transaction Tracking")
            print()
            print("<L> Log Out")
            
            menu = input("Opt >> ").strip().upper()
            if menu.upper() == "L":
                print("Exiting User View. Goodbye!")
                repeat = False
                
            elif menu == "1":
                update_user_profile(email_login)

            elif menu == "2":
                book_transaction(email_login)
                
            else:
                print("Invalid selection. Please try again.")

def edit_book_metadata(dd,booklist,email_login): 
    repeat = True
    while repeat:
        print("-"*50)
        print("<A>dd    Book")
        print("<U>pdate Book Info")
        print("<D>elete Book")
        print()
        print("<R>eturn")
        action = input("\n>> ").upper()
        
        if action == "A":
            dd = add_books(dd, booklist)
        elif action == "U":
            dd = edit_book(dd, booklist)
        elif action == "D":
            dd = delete_book(dd, booklist)
        elif action == "R":
            print("-"*50)
            print("Returning to previous menu...")
            repeat = False
        else:
            print("Invalid selection!")
        
def management(email_login):
    
    repeat = True

    while repeat:
        print("-"*50)
        print("----- Book Tracking and Inventory Management -----")
        print("                 Admin View")
        
        print("-"*50)
        print("\t<1> Edit Book Metadata")
        print("\t<2> Book Info List")
        print()
        print("\t<R> eturn")
        selection = input("\n>> ").upper()
        
        if selection == "1":
            edit_book_metadata(dd,booklist,email_login)
        
        elif selection == "2":
            book_info_list()
            
        elif selection == "R":
            print("-"*50)
            print("Returning to previous menu...")
            repeat = False
            
        else:
            print("-"*50)
            print("Invalid selection!")

def main_menu(): 
    
    load_user_info()
    load_book_info()

    repeat = True
    while repeat:
        print("-"*70)
        print("\t\t Welcome to XXLibrary System")
        print("\t\t\t Main Menu")
        print("-"*70)
        print("<1> Login \t\t <2> New User \t\t <Q> Quit System")
        print("-"*70)
        opt = input("Opt >> ")

        if opt == "1":
            login_user()
                
        elif opt == "2":
            register_user_info(users)
            
        elif opt.upper() == "Q":
            print("Exiting the system. Goodbye!")
            repeat = False
        
        else:
            print("Invalid option. Please try again.\n")
            

main_menu()
