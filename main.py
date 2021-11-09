# Brian D. Christman
# Purpose: To import the pets database from sql and allow users to select a pet from the database and
# learn more about them. They also have the option to edit the name and age of a pet if they wish. 

# See https://pymysql.readthedocs.io/en/latest/index.html
#  We need to install the mypysql library
#  In the Terminal window (bottom of PyCharm), run
#  pip3 install pymysql

# Import all packages and information required for this program
import pymysql.cursors
from creds import *
from petchooser import *

# Create the pets dictionary and list for all pet id numbers
petsDict = {}
idList = []

# Define petsMenu function which will list the pets in the database and their corresponding id
# Fill in the idList with the pet id numbers
def petsmenu():
    for id in petsDict:
        print(f"[{id}] {petsDict[id].getname()}")
        idList.append(id)
    print(f"[Q] Quit")

# Define the petsData function which will read in the data from sql and store it in a dictionary
def petsdata():
    # Our sql statement, easy to read
    petsSelect = """
      Select pets.name as name, pets.id as id, pets.age as age, owners.name as owner, 
      types.animal_type as animal from pets join owners on pets.owner_id = owners.id 
      join types on pets.animal_type_id = types.id;
      """
    # Execute select
    cursor.execute(petsSelect)

    # Loop through all the results and store in dictionary
    for row in cursor:
        petinfo = pets(name=row['name'],
                       id=row['id'],
                       age=row['age'],
                       owner=row['owner'],
                       animal=row['animal'])
        petsDict[row['id']] = petinfo

# Connect to the database and alert if something goes wrong. Reads info from creds.py.
try:
    myConnection = pymysql.connect(host=hostname,
                                   user=username,
                                   password=password,
                                   db=database,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

except Exception as e:
    print(f"An error has occurred. Cannot connect to the database. You have entered incorrect credentials.")
    print()
    exit()

# In the database, print and loop through the pet selection menu
try:
    with myConnection.cursor() as cursor:
        # ==================
        # Get and store the pets data in a dictionary
        petsdata()

        # NOTE: We are using placeholders in our SQL statement
        #  See https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        petsAgeEdit = """
            update
              pets
            set
              age = %s
            where
              id = %s;
            """
        petsNameEdit = """
            update
              pets
            set
              name = %s
            where
              id = %s;
            """

        # Print the instructions to the pet selection menu and print the selection menu
        print("Welcome to the pet selection menu!")
        print("To learn more about one of the pets, enter the number found to left of their name.")
        print("To quit and exit the menu, enter 'Q' or 'q' in the selection prompt at any time.")
        petsmenu()

        # Define stopping values and allow user to choose the pet they'd like to learn about
        stop = ['Q', 'q']
        cont = ['C', 'c']
        edit = ['E', 'e']
        petSelection = input("Please enter the number of the pet you'd like to learn about: ")

        # Loop through the responses. If the choice is valid print the pet information
        # If the choice is to stop, stop the program. Otherwise, have the user choose again
        # Always show the selection table to the user again so they can better make their choice
        # Additionally, the user can choose to edit the name and age of a pet if they wish
        while True:
            if petSelection in stop:
                print("Thank you for learning about our pets! We hope to see you again!")
                break
            elif petSelection in cont:
                petsmenu()
                petSelection = input("Please enter the number of the pet you'd like to learn more about: ")
            elif petSelection in edit:
                petsmenu()
                petChosen = input("Please enter the number of the pet you'd like to edit: ")
                if petChosen in stop:
                    print("Thank you for learning about our pets! We hope to see you again!")
                    break
                elif petChosen == '':
                    print("Your entry was not an integer corresponding to one of the pets.\n")
                elif not petChosen.isnumeric():
                    print("Your entry was not an integer corresponding to one of the pets.\n")
                elif int(petChosen) < 0:
                    print("Your entry was not an integer corresponding to one of the pets.\n")
                elif int(petChosen) and int(petChosen) in idList:
                    id = int(petChosen)
                    print(f"You have chosen to edit {petsDict[id].getname()}.")
                    print(f"To exit the edit process and close the program, enter 'QUIT' or 'quit' into either of the following prompts.\n")
                    editName = input("New name: [ENTER] == no change ")
                    newStop = ['QUIT','quit']
                    if editName in newStop:
                        break
                    elif editName != '':
                        cursor.execute(petsNameEdit, (editName, id))
                        myConnection.commit()
                        petsdata()
                        print("The pet's name has been updated!\n")

                    editAge = input("New age: [ENTER] == no change ")
                    while True:
                        if editAge in newStop:
                            petSelection = 'Q'
                            print()
                            break
                        elif editAge == '':
                            petsmenu()
                            petSelection = input("Please enter the number of the pet you'd like to learn more about: ")
                            break
                        elif not editAge.isnumeric() and editAge != '':
                            print("Your entry was not a positive integer corresponding to age.  Please try again.\n")
                            editAge = input("New age: [ENTER] == no change ")
                        elif int(editAge) < 0:
                            print("Your entry was not a positive integer corresponding to age.  Please try again.\n")
                            editAge = input("New age: [ENTER] == no change ")
                        elif int(editAge) >= 0:
                            cursor.execute(petsAgeEdit, (editAge, id))
                            myConnection.commit()
                            petsdata()
                            print("The pet's age has been updated!\n")
                            petSelection = 'C'
                            break
                        else:
                            petSelection = 'C'
                            print()
                            break
                else:
                    break
            elif not petSelection.isnumeric():
                print("Your entry was not an integer corresponding to one of the pets.\n")
                petsmenu()
                petSelection = input("Please enter the number of the pet you'd like to learn more about: ")
            elif int(petSelection) < 0:
                print("Your entry was not an integer corresponding to one of the pets.\n")
                petsmenu()
                petSelection = input("Please enter the number of the pet you'd like to learn more about: ")
            elif int(petSelection) and int(petSelection) in idList:
                id = int(petSelection)
                print(f"You have chosen {petsDict[id].getname()}, the {petsDict[id].getage()} year old {petsDict[id].getanimal()} owned by {petsDict[id].getowner()}.\n")
                petSelection = input("Would you like to [C]ontinue, [Q]uit, or [E]dit this pet? ")
            else:
                print("Your entry was not an integer corresponding to one of the pets.\n")
                petsmenu()
                petSelection = input("Please enter the number of the pet you'd like to learn more about: ")

# Check for errors. If something went wrong, print what went wrong
except Exception as e:
    print(f"A non-integer was entered that did not correspond to one of the pets and also forced the program to close.")
    print()

# Close connection
finally:
    myConnection.close()
    print("Connection closed.")
