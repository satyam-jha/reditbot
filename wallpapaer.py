import praw
import requests
import os
import smtplib
import imghdr
from email.message import EmailMessage
import cf
import dropbox


def get_link(sub_name):
    wallpapers = []

    reddit = praw.Reddit(client_id=cf.client_id,
                         client_secret=cf.secret,
                         user_agent="wallpaper bot")

    subreddit1 = reddit.subreddit(sub_name)

    for post in subreddit1.hot(limit=10):
        wallpapers.append(post.url)

    return wallpapers


def dropupload(wallpapers, token, email_address):
    msg = EmailMessage()
    msg['Subject'] = 'Todays top 10 wallpapers'
    msg['To'] = email_address
    msg['From'] = cf.user_email
    msg.set_content("Todays Top wallpapers are")
    for img in wallpapers:
        img_data = requests.get(img).content

        file_to = '/wallpaper/{}'.format(img.split('/')[-1])
        a = img.split('/')[-1]
        drop = dropbox.Dropbox(token)
        drop.files_upload(img_data, file_to)

        file_data = img_data
        file_type = a.split('.')[-1]
        file_name = img.split('/')[-1]
        # print(file_type)
        if file_data != None:
            msg.add_attachment(file_data, maintype='image',
                               subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user=cf.user_email, password=cf.user_pass)
        smtp.send_message(msg)


def download(wallpapers):
    for img in wallpapers:
        img_data = requests.get(img).content
        print(type(img_data))
        with open(os.path.join("wallpaper", img.split('/')[-1]), 'wb') as f:
            f.write(img_data)


def sendmail(images, email_address):
    msg = EmailMessage()
    msg['Subject'] = 'Todays top 10 wallpapers'
    msg['To'] = email_address
    msg['From'] = cf.user_email
    msg.set_content("Todays Top wallpapers are")

    for img in images:
        print(type(img))
        with open(os.path.join("wallpaper", img), 'rb') as i:
            print(type(i))
            file_data = i.read()
            file_type = imghdr.what(i.name)
            file_name = i.name
            print(type(file_data))
            # print(file_type)
            if file_type != None:
                msg.add_attachment(file_data, maintype='image',
                                   subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user=cf.user_email, password=cf.user_pass)
        smtp.send_message(msg)


def runtasks(sub, email, token):

    images = get_link(sub_name=sub)

    data = []
    for img in images:
        data.append(img.split('/')[-1])
    dropupload(wallpapers=images, token=token, email_address=email)
    # download(wallpapers=images)
    #sendmail(data, email_address=email)
