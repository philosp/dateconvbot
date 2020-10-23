import os # for file path operations

# Set up the directories based on the current location of the script.
# Fetch the absolute directory the script is in.
HOME_PATH = os.path.dirname(os.path.realpath(__file__))

LOG_FILE = HOME_PATH+"/DateConvBot.log"

DB_FILE = HOME_PATH+"/sqlite.db"

#these have the same names as the convertdate modules 
AVAILABLE_CALENDARS = ('armenian', 'bahai', 'chinese', 'coptic', 'dublin',
        'french_republican', 'gregorian', 'hebrew',
        'indian_civil', 'islamic', 'iso',
        'julian', 'mayan', 'persian', 'positivist')

SYNTAX_TIPS = '''

Syntax: !dateconv _fromCalendar_ _toCalendar_ **YYYY.MM.DD**  
   or !dateconv today _toCalendar_ 

Available calendars: 
'''

SYNTAX_TIPS += ', '.join(AVAILABLE_CALENDARS)

MONITORED_SUBS = ('u_DateConvBot','translator','TranslationStudies','LanguageLearning','hebrew','judaism')

# Different transliterations and spellings 
HEBREW_MONTHS = {
        'TISHRI': 7,
        'TISHREI': 7,
        'HESHVAN': 8,
        'CHESHVAN': 8,
        'MARHESHVAN': 8,
        'MARCHESHVAN': 8,
        'KISLEV': 9,
        'TEVET': 10,
        'TEVETH': 10,
        'SHVAT': 11,
        'SHEVAT': 11,
        'ADAR': 12,
        'ADAR1': 12,
        'ADARI': 12,
        'ADARALEF': 12,
        'VEADAR': 13,
        'ADAR2': 13,
        'ADARII': 13,
        'ADARBET': 13,
        'NISAN': 1,
        'NISSAN': 1,
        'YIAR': 2,
        'IYAR': 2,
        'IYYAR': 2,
        'SIVAN': 3,
        'TAMUZ': 4,
        'TAMMUZ': 4,
        'AV': 5,
        'MENACHEMAV': 5,
        'ELLUL': 6,
        'ELUL': 6
}

HEBREW_RESULT = {
        7: 'TISHREI',
        8: 'CHESHVAN',
        9: 'KISLEV',
        10: 'TEVET',
        11: 'SHEVAT',
        12: 'ADAR',
        13: 'ADAR BET',
        1: 'NISAN',
        2: 'IYAR',
        3: 'SIVAN',
        4: 'TAMUZ',
        5: 'AV',
        6: 'ELUL'
}
