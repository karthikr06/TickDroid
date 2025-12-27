#setup everything here
import os
import time
import json

def reset():
    print("Are you sure you want to reset the bot? This will delete all data. (y/n)")
    choice=input().lower()
    if choice=="y":
        with open("json/botmods.json", "w") as f:
            f.write('{\n    "admin":[],\n    "webookURL":""\n}')
        with open("json/control.json", "w") as f:
            with open("json/defaultServer.json", "r") as r:
                f.write(r.read())

def integrityCheck():
    with open("json/control.json", "r") as f:
        data=json.load(f)
    if "prefix" not in data or "Features" not in data:
        print("control.json is corrupted. Do you want to reset it? (y/n)")
        choice=input().lower()
        if choice=="y":
            reset()
        else:
            print("Check /json/control.json and fix the issue manually.")
        time.sleep(2)
    else:
        print("control.json passed the integrity check.")
        time.sleep(1)
    print("Checking server specific files...")
    time.sleep(2)
    try:
     for file in "json/server":
        with open(file, "r") as f:
            data=json.load(f)
        if "prefix" not in data or "Features" not in data:
            print(f"{file} is corrupted. Do you want to reset it? (y/n)")
            choice=input().lower()
            if choice=="y":
                with open("json/defaultServer.json", "r") as r:
                    with open(file, "w") as f:
                        f.write(r.read())
                print("File reset.")
            else:  
                print(f"Check {file} and fix the issue manually.")
                time.sleep(1)
    except FileNotFoundError:
        print("No server specific files found. Skipping this step.")
        time.sleep(1)
    print("Integrity check complete. Fix the errors(if any) and restart the bot.")

def setup():
    print("Welcome to TickDroid 2.0 setup!")
    print("Performing a file check...")
    time.sleep(2)
    required_files = [
        "json/botmods.json",
        "json/control.json",
    ]
    file="json/defaultServer.json"

    print("Setting the default configuration file...")
    with open(file, "w") as f:
        f.write('''{
    "prefix": "t-",
    "Features": {
        "ping":true,
        "8ball": true,
        "gemini": true,
        "onMessage": true,
        "AImemory": true
    },
    "AI_memory":[]
}''')
        
    for file in required_files:
        if not os.path.exists(file):
            print(f"Missing file: {file}. Creating default.")
            if file == "json/botmods.json":
                with open(file, "w") as f:
                    f.write('{\n    "admin":[],\n    "webookURL":"",\n   "gemini_api_key": "",\n   "bot_token":""\n }')
            elif file == "json/control.json":
                with open(file, "w") as f:
                    with open("json/defaultServer.json", "r") as r:
                        f.write(r.read())
    time.sleep(2)
    print("File check complete.")
    print("Entering main setup...")
    time.sleep(1)
    print("Enter bot admin user Discord ID: (the one who can edit the bot settings)")
    print("You can add more admins later by editing json/botmods.json")
    adminID=input("Admin Discord ID: ")
    print("Enter webhook URL for bot logs: ")
    webhookURL=input("Webhook URL: ")
    with open("json/botmods.json", "r") as f:
        f=json.load(f)
    with open("json/botmods.json", "w") as file:
        f["admin"]=[int(adminID)]
        f["webookURL"]=webhookURL
        json.dump(f, file, indent=4)
    print("Setup complete! You can now run the bot.")
    print("<mention the bot>setup to add server information to the bot database if it is not added automatically.")
    print("Read the readME file for more information.")

integrityCheck()