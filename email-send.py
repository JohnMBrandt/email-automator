# -*- coding: utf-8 -*-
__author__ = 'johnbrandt'
import csv
import smtplib
from random import randint
from datetime import datetime
from threading import Timer
import socket
import threading
import imaplib
import email

#the following code is where you input the different messages you would like to send
#it is also possible to schedule these messages to send at random days
# the responses will be stored on gmails server that can be downloaded into python with gmail api
#these would be parsed with a different script


print(chr(27) + "[2J")

run = 1

messagespositive = {1:"Think of a moment when you found yourself in uncontrollable laughter at something someone said. What word describes what made you laugh?", 2:"What is one movie, or even TV show, that you find particularly funny? Tell us!", 3:"\nSend us a one-word descriptor of what you think about this GIF: http://giphy.com/gifs/editor-funny-gif-cat-gifs-mnyMpAyg1fB9C", 4:"\nSend us a one-word descriptor of what you think about this GIF: http://giphy.com/gifs/soccer-running-qxYkv4GuyYbbG", 5:"Please check your mailbox! Let us know what you find.", 6:" What is one time when you had an outcome that was better than expected and made you smile? Text us back one word about that experience.", 7:"Imagine that someone did something unexpectedly nice for you. What would it be? Tell us in three or fewer words.", 8:"Think of a time where you sought out to be surprised (eg. going to an amusement park). Describe the event.", 9:"Imagine that your friends throw you the perfect surprise party for your birthday. Where would it take place?", 10: "Take a moment to think deeply about a time when you felt particularly interested in something. Give us one word relating to that moment.", 11: "Tell us in a few words, what is one thing that you found to be especially interesting during one of your classes here at Vassar?", 12: "Think back to a time when you were watching a film or TV show that really caught your interest. What is its title?", 13: "There are many amazing things in this world. What is one thing you would like to further explore? Please tell us in three words or less.", 14: "Glass can be made from almost anything if molten material cools before its molecules realign into what it once was.Have you ever made glass?", 15: "What is one department at Vassar in which you have always been interested in taking a class, but never got around to doing so?", 16: "What is one skill you want to learn just out of interest and not necessity?", 17: "Think of a fact that you find particularly interesting. What is it?", 18: "Think of someone that has helped you out before, let us know who they are, and then let them know that you appreciate them.", 19:"Think of a group of people who you can rely on to help you--tell us, who are they? And how might you express your gratitude for their help?", 20:"Think of a time when you felt especially grateful for someone. Tell us briefly who that person is, and why you were grateful for them.", 21: "Think of a time when you were very grateful for something someone did for you. Tell us in one word how you'd express this gratitude to them.", 22: "Think of an experience you were very fortunate to have (e.g. job, school). Tell us about it in 3 words or less.", 23: "What have you done, or what could you do, to show appreciation towards another person? Tell us in three words or less.", 24: "Think of something you are grateful for that has occurred in the past 24 hours. Describe it to us in one word.", 25: "Think of yourself doing an activity that relaxes you. In one word, what would you be doing?", 26: "\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/beach-IWHBAEKT9udiM", 27: "\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/nowthisnews-flowers-chile-atacama-yNZ8VwWPOBcUE", 28: "\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/sunrise-sun-WzLDljBpplUvm", 29: "\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/aurora-borealis-dreaming-northern-lights-oNb3GLUvhF768", 30: "\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/sky-birds-LeoQs1lygBc1W"}


messagesneutral = {1:"Think back to a moment when you were walking on a pathway on campus. Do you remember what season it was? Let us know.", 2:"Name the first movie or tv show that pops into your head.", 3:"\nSend us a one-word descriptor of what you think of this video: https://www.youtube.com/watch?v=COGTCGZ3I6U", 4:"\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/B0Gfpxgbek1LW", 5:"Imagine you have a note waiting for you in your mailbox. Off the top of your head, let us know what you think it says.", 6:"Think of the outcome to a recent situation. Text us back one word relating to that situation.", 7:"Tell us, in three or fewer words, about one nice thing someone once did for you.", 8:"When was the last time you went out to see a movie?", 9:"Name the first location that comes to mind.", 10:"Think of your daily routine and text us one word about it.", 11:"Tell us, what is one class that you have taken during your time at Vassar?", 12:"Think back to a time when you were watching a movie or tv show? Where did you watch it?", 13:"What is something that was recently made? Please tell us in three or fewer words.", 14:"Did you know that Alabama’s state flower is the camellia? Have you ever been to Alabama? Let us know with a yes or a no.", 15:"In what department have you taken the most classes at Vassar?", 16:"In your opinion, what is one necessary life skill that everyone should learn to do?", 17:"Think about something to distract yourself. Let us know what it is.", 18:"Think about a large group of people you saw in the past. Where did you see them? Tell us in less than 3 words.", 19:"Take a moment to count the number of people there are near you in your current location. How many are there?", 20:"Think of a time when you interacted with someone. Was it in person, over the phone, skype, or messaging?", 21:"Think of something you recently obtained. Tell us about it in three or fewer words.", 22:"Think of something you recently did with another person (e.g. watched movie). Please tell us about it in three or fewer words.", 23:"Think of something that you've eaten in the past 24 hours. What was it?", 24:"Envision yourself unpacking a bag. What did you just take out?", 25:"\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/gfaught-loop-colors-3o85xEIe1YKaGrSvhC", 26:"\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/gfaught-loop-color-cubes-xTiTnnh31rfsSu79Pq", 27:"\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/design-wiggle-pattern-lXiRpvD4Bfp1VOKUo", 28:"\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/google-use-smartphone-DVkRdAYY5OXjW", 29:"\nSend us a one-word descriptor of what you think of this GIF: http://giphy.com/gifs/loop-design-CfekPiljFLSpy"}


#the following code chooses one of the above messages at random



#the following code is where you store the different phone numbers
positivephonenumbers = ['REPLACE W PHONE NUMBERS']

neutralphonenumbers = ['REPLACE W PHONE NUMBERS']
#the following code lets you log in to a gmail account
#this sends a random message
def sendpositive():
    number = randint(1,31)
    message2send = messagespositive[number]
    socket.setdefaulttimeout(12000)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    #use any gmail username and password
    server.login('EMAIL', 'PASSWORD')
    server.sendmail('EMAIL', positivephonenumbers, message2send)

def sendneutral():
    numberneutral = randint(1,29)
    messageneutral2send = messagesneutral[numberneutral]
    socket.setdefaulttimeout(12000)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    #use any gmail username and password
    server.login('EMAIL', 'PASSOWRD')
    server.sendmail('EMAIL', neutralphonenumbers, messageneutral2send)

randtime = randint(2,3)
randmin = randint(1,60)
timesent = randtime*360+randmin*60
totaltime = timesent/1200
timesent2 = timesent * 2
timesent3 = timesent * 3
print "The text will be sent every %i hours and %i minutes for a total of 3 times, ending in %i hours." %(randtime, randmin, totaltime)
    ###mininput = int(raw_input("How many minutes away?"))
def work1():
    threading.Timer(timesent, sendpositive).start()
    threading.Timer(timesent, sendneutral).start()
def work2():
    threading.Timer(timesent2, sendpositive).start()
    threading.Timer(timesent2, sendneutral).start()
def work3():
    threading.Timer(timesent3, sendpositive).start()
    threading.Timer(timesent3, sendneutral).start()
work1()
work2()
work3()


