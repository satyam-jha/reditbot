from .wallpapaer import runtasks
import schedule
import time

email = "10satyam.jha@gmail.com"

sub = "wallpapers"

schedule.every().day.at("1:00").do(runtasks, sub=sub, email=email)

while True:
    schedule.run_pending()
    time.sleep(1)
