import praw
import requests
import os
import smtplib
import imghdr
from email.message import EmailMessage
import cf


def get_link(sub_name):
    wallpapers = []

    reddit = praw.Reddit(client_id=cf.client_id,
                         client_secret=cf.secret,
                         user_agent="wallpaper bot")

    subreddit1 = reddit.subreddit(sub_name)

    for post in subreddit1.hot(limit=10):
        wallpapers.append(post.url)

    return wallpapers


def download(wallpapers):
    for img in wallpapers:
        img_data = requests.get(img).content
        with open(os.path.join("wallpaper", img.split('/')[-1]), 'wb') as f:
            f.write(img_data)


def sendmail(images, email_address):
    msg = EmailMessage()
    msg['Subject'] = 'Todays top 10 wallpapers'
    msg['To'] = email_address
    msg['From'] = cf.user_email
    msg.set_content("Todays Top wallpapers are")

    for img in images:
        with open(os.path.join("wallpaper", img), 'rb') as i:
            file_data = i.read()
            file_type = imghdr.what(i.name)
            file_name = i.name
            print(file_type)
            if file_type != None:
                msg.add_attachment(file_data, maintype='image',
                                   subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user=cf.user_email, password=cf.user_pass)
        smtp.send_message(msg)


def runtasks(sub, email):

    images = get_link(sub_name=sub)

    data = []
    for img in images:
        data.append(img.split('/')[-1])

    download(wallpapers=images)
    sendmail(data, email_address=email)
