from main.wallpaper import runtasks, dropupload
import schedule
import time

# email = "10satyam.jha@gmail.com"

# sub = "wallpaper"

# token = "_FBBaBWz2GgAAAAAAAAAAYj4SOFZAwEAL-ECw4uVVjriywQoZNbAv67zzPnUCSU6"

#improve code remove hardcoded values from code 

#TODO use db to store emails and time

def sayhello(): #FIXME
    print("hello")

sayhello()
runtasks(sub=sub, email=email, token=token)
#schedule.every().day.at("10:46").do(runtasks, sub=sub, email=email, token=token)

# while True:
#    schedule.run_pending()
#   time.sleep(1)
