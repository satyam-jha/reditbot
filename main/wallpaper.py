from http import client
import re
from praw import Reddit
import requests
import os
import smtplib
import imghdr
from email.message import EmailMessage
import cf
import dropbox
from dotenv import load_dotenv

load_dotenv()

"""
#TODO Need to optimise code 
#TODO Need to add DataBase to store emails
#TODO Need to add functionality to get other things then wallper
#TODO Need to add Option to make library on dropbox

"""


class RedditPosts():
    def __init__(self, sub_name):
        self.sub_name = sub_name
        self.client_id = os.getenv('CLIENT_ID')
        self.secret = os.getenv('SECRET')
        self.user_agent = os.getenv('USER_AGENT')
        self.user_name = os.getenv('USER_NAME')
        self.password = os.getenv('PASSWORD')
        self.user_email = os.getenv('USER_EMAIL')
        self.user_pass = os.getenv('USER_PASS')

    def get_links(self):
        wallpapers = []
        reddit = Reddit(client_id=self.client_id, client_secret=self.secret,
                        username=self.user_name, user_agent=self.user_agent, password=self.password)

        sub_reddit = reddit.subreddit(self.sub_name)

        for post in sub_reddit.hot(limit=10):
            wallpapers.append(post.url)

        return wallpapers

    def sendmail(self, image_links, email_address):
        msg = EmailMessage()
        msg['Subject'] = 'Todays top 10 wallpapers'
        msg['To'] = email_address
        msg['From'] = self.user_email
        msg.set_content("Todays Top wallpapers are")

        for link in image_links:
            img_data = requests.get(link).content
            file_data = img_data
            file_name = link.split('/')[-1]
            file_type = file_name.split('.')[-1]

            if file_type != None:
                msg.add_attachment(file_data, maintype='image',
                                   subtype=file_type, filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            print(self.user_email + " " + self.user_pass)
            smtp.login(user=self.user_email, password=self.user_pass)
            smtp.send_message(msg)

            return f'Email has been sent to {email_address}'


wallpapers = RedditPosts(sub_name='wallpaper')
links = wallpapers.get_links()
wallpapers.sendmail(image_links=links, email_address=[
    '10satyam.jha@gmail.com', 'jha.satyam7@gmail.com'])


# def get_link(sub_name):
#     wallpapers = []

#     reddit = Reddit(client_id=cf.client_id,
#                     client_secret=cf.secret,
#                     user_agent="wallpaper bot")

#     subreddit1 = reddit.subreddit(sub_name)

#     for post in subreddit1.hot(limit=10):
#         wallpapers.append(post.url)

#     return wallpapers


# def dropupload(wallpapers, token, email_address):
#     msg = EmailMessage()
#     msg['Subject'] = 'Todays top 10 wallpapers'
#     msg['To'] = email_address
#     msg['From'] = cf.user_email
#     msg.set_content("Todays Top wallpapers are")
#     for img in wallpapers:
#         img_data = requests.get(img).content

#         file_to = '/wallpaper/{}'.format(img.split('/')[-1])
#         a = img.split('/')[-1]
#         drop = dropbox.Dropbox(token)
#         drop.files_upload(img_data, file_to)

#         file_data = img_data
#         file_type = a.split('.')[-1]
#         file_name = img.split('/')[-1]
#         # print(file_type)
#         if file_data != None:
#             msg.add_attachment(file_data, maintype='image',
#                                subtype=file_type, filename=file_name)

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(user=cf.user_email, password=cf.user_pass)
#         smtp.send_message(msg)


# def download(wallpapers):
#     for img in wallpapers:
#         img_data = requests.get(img).content
#         print(type(img_data))
#         with open(os.path.join("wallpaper", img.split('/')[-1]), 'wb') as f:
#             f.write(img_data)


# def sendmail(images, email_address):
#     msg = EmailMessage()
#     msg['Subject'] = 'Todays top 10 wallpapers'
#     msg['To'] = email_address
#     msg['From'] = cf.user_email
#     msg.set_content("Todays Top wallpapers are")

#     for img in images:
#         print(type(img))
#         with open(os.path.join("wallpaper", img), 'rb') as i:
#             print(type(i))
#             file_data = i.read()
#             file_type = imghdr.what(i.name)
#             file_name = i.name
#             print(type(file_data))
#             # print(file_type)
#             if file_type != None:
#                 msg.add_attachment(file_data, maintype='image',
#                                    subtype=file_type, filename=file_name)

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(user=cf.user_email, password=cf.user_pass)
#         smtp.send_message(msg)


# def runtasks(sub, email, token):

#     images = get_link(sub_name=sub)

#     data = []
#     for img in images:
#         data.append(img.split('/')[-1])
#     dropupload(wallpapers=images, token=token, email_address=email)
#     # download(wallpapers=images)
#     #sendmail(data, email_address=email)
