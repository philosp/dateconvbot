# DateConvBot
DateConvBot is a bot monitoring Reddit comments to help convert dates between calendars

It uses the [PRAW](https://github.com/praw-dev/praw) module to access Reddit.

It uses the [Convertdate](https://github.com/fitnr/convertdate) module for date conversions.
Note that in some calendar systems, the day begins at sundown. Convertdate gives the conversion for noon of the day in question. 
For more details, please refer to Convertdate's Readme.

Usage and syntax:

  - To summon the Bot, make a comment in any post in one of the monitored subs, with 1 line starting with "!dateconv" (no quotes).
  - The syntax is:  
    !dateconv _fromCalendar_ _toCalendar_ **YEAR.MONTH.DAY**  
    or   
    !dateconv **today** _toCalendar_  

Monitored Subreddits:
  - [r/translator](https://old.reddit.com/r/translator)
  - [r/TranslationStudies](https://old.reddit.com/r/TranslationStudies)
  - [r/LanguageLearning](https://old.reddit.com/r/LanguageLearning)
  - [r/hebrew](https://old.reddit.com/r/hebrew)
  - [r/judaism](https://old.reddit.com/r/judaism)
  - and the bot's own user page ([u/DateConvBot](https://old.reddit.com/user/DateConvBot))

Available calendars:
  - Armenian
  - Bahai
  - Coptic (Alexandrian)
  - French Republican
  - Gregorian
  - Hebrew
  - Indian Civil
  - Islamic
  - Julian
  - Mayan
  - Persian
  - Positivist
  - Mayan
  - ISO
