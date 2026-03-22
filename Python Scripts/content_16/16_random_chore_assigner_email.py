import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import keyring

"""
Script 16_random_chore_assigner_email.py references a list of emails to assign a chores.
"""

## Find 16_chores.txt, 16_chore_contacts.txt, and 16_chore_history filepaths

def get_filepaths(pDirectory,pFileDictionary):

    vFilepathDictionary = {}

    for folderpath,subfolder,filenames in os.walk(pDirectory):
        
        for key,filename in pFileDictionary.items():

            if filename in filenames:
                vFilepathDictionary[key] = os.path.join(folderpath,filename)

    return vFilepathDictionary    

## extract data from text files
def read_file(pFilepath):
    with open(pFilepath,'r') as file:

        file_content = [line.strip("\n") for line in file]

        return file_content

## Get last run date
def parse_history(history_lines):

    history = []

    for line in history_lines:
        name, email, chore, timestamp = line.split(",")

        history.append({
            "chore": chore,
            "name": name,
            "email": email,
            "timestamp": timestamp
        })

    return history

def get_last_run(history):

    if not history:
        return []

    timestamps = [
        datetime.strptime(row["timestamp"], "%m-%d-%Y %H:%M")
        for row in history
    ]

    latest_time = max(timestamps)

    last_run = [
        row for row in history
        if datetime.strptime(row["timestamp"], "%m-%d-%Y %H:%M") == latest_time
    ]

    return last_run

def build_blacklist(last_run):

    blacklist = set()

    for row in last_run:
        blacklist.add((row["name"], row["chore"]))

    return blacklist

## Email contact (Load)    

def draft_email(pSender,pReceivier,pName,pChore):
    # --- Create Message ---
    message = MIMEMultipart()
    message["From"] = pSender
    message["To"] = pReceivier
    message["Subject"] = f"Chore Assignment for {pName}"
    body = f"Hello {pName},\n\nYour chore assignment is {pChore}"
    message.attach(MIMEText(body, "plain"))

    return message

def send_email(pSender,pSenderPwd,pReceivier,pMessage):
    # --- Send Email ---
    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() # Secure the connection
        server.login(pSender, pSenderPwd)
        server.sendmail(pSender, pReceivier, pMessage.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def main():

    directory = os.getcwd()

    vSender = keyring.get_password("system", "test_email")
    vSenderPwd = keyring.get_password("system", vSender)
    
    FILES = {
    "Contacts": "16_chore_contact.txt",
    "Chores": "16_chore_list.txt",
    "History": "16_chore_history.txt"
    }

    vFilepaths = get_filepaths(directory,FILES)

    Contacts = read_file(vFilepaths["Contacts"])
    Chores = read_file(vFilepaths["Chores"])
    HistoryLines = read_file(vFilepaths["History"])

    History = parse_history(HistoryLines)
    LastRun = get_last_run(History)
    Blacklist = build_blacklist(LastRun)

    ## Assign random chore to contact (Transform)
    formatted_date = datetime.now().strftime("%m-%d-%Y %H:%M")

    with open(vFilepaths["History"], "a") as file:

        while Chores:

            made_assignment = False
            random.shuffle(Contacts)
            random.shuffle(Chores)
            
            for contact,chore in zip(Contacts,Chores):
                
                name, email = contact.split(',')

                if (name, chore) in Blacklist:
                    print(f"Skipping {name} for {chore}")
                    continue
                
                line = f"{contact},{chore},{formatted_date}\n"
                print(line)
                file.write(line)

                ##Send Email
                vReceiver = email
                vMessage = draft_email(vSender,vReceiver,name,chore)

                send_email(vSender,vSenderPwd,vReceiver,vMessage)

                Contacts.remove(contact)
                Chores.remove(chore)
                
                made_assignment = True

            if made_assignment == False:
                break

main()


