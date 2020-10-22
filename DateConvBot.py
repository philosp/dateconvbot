import time # for sleeping
import re # for Regular Expressions
import praw # Python Reddit API Wrapper (https://github.com/praw-dev/praw)
import convertdate # date conversion library (https://github.com/fitnr/convertdate)
from datetime import datetime # for today's date and seconds to date conversion
import importlib # used to import the correct Object based on the calendar name
import sqlite3 # lightweight serverless local database
import logging # logging functions
from logging.handlers import RotatingFileHandler # logging to file

#importing local settings
import secrets
from config import *

# root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create a file logger
handler = RotatingFileHandler(LOG_FILE, maxBytes=1024*1024*1, backupCount=3)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# RegularExpression Pattern that matches any digit, used in the main loop
redigits = re.compile('[0-9]',re.IGNORECASE)

def db_comment_exists(comment_id):
    cur = con.cursor()
    qry = "SELECT count(*) FROM SEEN_COMMENTS WHERE comment_id = ? "
    cur.execute(qry,(comment_id,))
    res = cur.fetchone()
    cur.close()
    if res[0] == 0:
        return False
    else:
        return True

def db_store_comment(comment):
    cur = con.cursor()
    qry = "INSERT INTO SEEN_COMMENTS (comment_id,seen_date,subreddit) VALUES(?,?,?) "
    cur.execute(qry,comment)
    con.commit()
    res = cur.lastrowid
    cur.close()
    return res

def db_store_reply(reply):
    cur = con.cursor()
    qry = "INSERT INTO REPLIES (id_seen_comment,from_calendar,to_calendar,julian_day) VALUES(?,?,?,?) "
    cur.execute(qry,reply)
    res = cur.lastrowid
    qry = "UPDATE SEEN_COMMENTS SET has_reply=1 WHERE id = ?"
    cur.execute(qry,(reply[0],))
    con.commit()
    cur.close()
    return res

def run_bot(r,mon_sub):
    sub = r.subreddit(mon_sub)
    posts = []
    #Get comments list
    posts += list(sub.comments(limit=99))
    logger.debug(f"Comment list in {mon_sub}: {len(posts)}")
    
    #Iterating through all retrieved comments 
    for comment in posts:

        #Comment already in SEEN_COMMENTS, get next one
        if db_comment_exists(comment.id):
            logger.info(f"ID {comment.id} already exists!")
            continue
        
        logger.debug(f"Comment id: {comment.id}, made in {datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')}")
        #Store the comment in SEEN_COMMENTS
        stored_id = db_store_comment((comment.id,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),mon_sub))
        logger.debug(f"Stored under id: {stored_id}")
        
        #Iterating through every line in the comment
        for line in comment.body.splitlines(): 
            #Set all characters to lowercase, then remove all surrounding spaces and tabs
            line = line.lower().strip()
            if line.startswith("!dateconv"):
                print(f"Summoned by comment: '{comment.id}'!")
                logger.info(f"Summoned by comment: '{comment.id}'!")
                logger.debug(line)
                #split the text along the spaces, creating "words"
                # the expected format is:
                # word 0 = !dateconv
                # word 1 = fromCalendar (or today)
                # word 2 = toCalendar
                # word 3 = the Date (if not today)
                words = line.split()
                size = len(words)
                if size >= 3:
                    FROM_OK = 0
                    from_calendar = words[1]
                    to_calendar = words[2]
                    if from_calendar in ("today","now"):
                        jd = convertdate.julianday.from_datetime(datetime.now())
                        FROM_OK = 1
                    # only allow predefined calendars
                    elif from_calendar in AVAILABLE_CALENDARS and size >= 4:
                        #looking for the separator character
                        #remove all digits, whatever is left in the first position is the separator
                        sep = redigits.sub('',words[3])
                        if len(sep) >=2:
                            #split the date along the separator character
                            date = words[3].split(sep[0])
                            if len(date) == 3:
                                parts = []
                                try:
                                    for part in date:
                                        # In Hebrew calendar (in the convertdate module)
                                        # the numbers assigned to months are confusing (biblical style)
                                        # making the year start in month 7 instead of 1
                                        # therefore the lookup should be with the month name (see config.py)
                                        if from_calendar == "hebrew" and part.upper() in HEBREW_MONTHS.keys():
                                            parts.append(HEBREW_MONTHS.get(part.upper()))
                                        else:
                                            #attempt to convert the lookup string into number
                                            parts.append(int(part))
                                    # In order to access the correct conversion functions
                                    # use importlib to assemble the name of module
                                    module = importlib.import_module(f"convertdate.{from_calendar}")
                                    func = getattr(module,"to_jd")
                                    #always convert to JulianDay
                                    jd = func(parts[0],parts[1],parts[2])
                                    FROM_OK = 1
                                except Exception as e:
                                    logger.error("Unable to parse FROM date. Error: {}".format(str(e)))
                                    FROM_OK = 0
                    else:
                        logger.error("FROM command not available")
                        FROM_OK = 0
                    
                    # only follow to the next part if we managed to get a JulianDay in the first part
                    if FROM_OK == 1 and to_calendar in AVAILABLE_CALENDARS:
                        try:
                            #access the functions from the right module
                            module = importlib.import_module(f"convertdate.{to_calendar}")
                            func = getattr(module,"from_jd")
                            #convert from the JulianDay
                            result = func(jd)
                            #Assemble the result
                            if to_calendar == "hebrew":
                                # Looking for Hebrew month names, instead of the confusing numbers
                                s = f"Result: {result[2]} {HEBREW_RESULT.get(result[1]).title()} {result[0]}"
                            else:
                                s = "Result: {}".format(".".join("{0}".format(n) for n in reversed(result)))
                            logger.info(f"Replying to comment with '{s}'")
                            # Send the reply!
                            comment.reply(s)
                            # Store the reply in our local database, for reference
                            db_store_reply((stored_id,from_calendar,to_calendar,jd))
                        except Exception as e:
                            logger.error("Unable to parse TO date. Error: {}".format(str(e)))
                    else:
                        logger.error("TO command not available")
                        s = f"Couldn't understand your command... {SYNTAX_TIPS}"
                        comment.reply(s)
                elif len(words) > 1 and words[1]=="help":
                    logger.debug("HELP command issued")
                    s = f"DateConvBot {SYNTAX_TIPS}"
                    comment.reply(s)
                else:
                    logger.info("Too few arguments")
                    s = f"Too few arguments... {SYNTAX_TIPS}"
                    comment.reply(s)

# This connects to the main database
con = sqlite3.connect(DB_FILE)

co = 0
# the CRONTAB is setup to call this script every 30 minutes
# Loops through the robot 28 times, with 1 minute intervals
while(co < 28):
    #Login to Reddit
    r = praw.Reddit(username = secrets.username,
        password = secrets.password,
        client_id = secrets.client_id,
        client_secret = secrets.client_secret,
        user_agent = "/u/DateConvBot Converts Dates v0.1")
    # Iterating through our subs
    for mon_sub in MONITORED_SUBS:
        print(mon_sub)
        run_bot(r,mon_sub)
        print("Done looping!")
    # Take a break!
    time.sleep(60)
    co += 1
#close the database
con.close()
