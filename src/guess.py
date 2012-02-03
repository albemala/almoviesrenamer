# -*- coding: latin-1 -*-
import re
import datetime
import utils

__author__ = "Alberto Malagoli"

blackwords = [
              # video type
              'DVDRip', 'HD-DVD', 'HDDVD', 'HDDVDRip', 'BluRay', 'Blu-ray', 'BDRip', 'BRRip',
              'HDRip', 'DVD', 'DVDivX', 'HDTV', 'DVB', 'DVBRip', 'PDTV', 'WEBRip', 'DVDSCR',
              'Screener', 'VHS', 'VIDEO_TS',
              # screen
              '720p', '720',
              # video codec
              'XviD', 'DivX', 'x264', 'h264', 'Rv10',
              # audio codec
              'AC3', 'DTS', 'He-AAC', 'AAC-He', 'AAC', '5.1',
              # ripper teams
              'ESiR', 'WAF', 'SEPTiC', '[XCT]', 'iNT', 'PUKKA', 'CHD', 'ViTE', 'TLF',
              'DEiTY', 'FLAiTE', 'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS', ' FiNaLe',
              'UnSeeN', 'aXXo', 'KLAXXON', 'NoTV', 'ZeaL', 'LOL', 'iTALiAN'
              ]

def info(title):
    """
    given a title, tries to guess as much information as possible.
    
    guessed information:
    title, year, language, country, part
    
    language and country are pycountry classes
    """

    # create info dictionary
    info = dict()
    # guess year
    title, year = guess_year(title)
    if year != None:
        info.update({'year': year})
    # guess language
    title, language = guess_language(title)
    if language != None:
        info.update({'language': language})
    # guess part
    title, part = guess_part(title)
    if part != None:
        info.update({'part': part})
    # clean title
    title = clean_title(title)
    info.update({'title': title})
    # return guessed information
    return info

def guess_year(title):
    """
    looks for year patterns, and return found year
    
    note this only looks for valid production years, that is between 1920
    and now + 5 years, so for instance 2000 would be returned as a valid
    year but 1492 would not
    """

    year = None
    # search for year pattern (4 consequent digit)
    match = re.search(r'[0-9]{4}', title)
    # if found, check if year is between 1920 and now + 5 years
    if match \
    and 1920 < int(match.group(0)) < datetime.date.today().year + 5:
        year = match.group(0)
        # remove year from title
        title = title[:match.start()] + title[match.end():]
    return title, year

def guess_language(title):
    """
    guess movie language, looking for ISO language representation in title
    """

    language = None
    match = re.search('(?:[^A-Z])([A-Z]{3})(?:[^A-Z])', title)
    if match:
        try:
            print(match.group(1))
            language = utils.alpha3_to_language(match.group(1).lower())
            print(language.name)
            # remove language from title
            title = title[:match.start() + 1] + title[match.end() - 1:]
        except KeyError:
            pass
    return title, language

def guess_part(title):
    """
    guess movie part, i.e. CD1
    """

    part = None
    # search part, which can be like, for example, disk1 or disk 1
    match = re.search('(cd|disk|part)[ ]?[0-9]', title.lower(), re.IGNORECASE)
    if match:
        # get part number
        part = match.group(0)[-1:]
        # remove part from title
        title = title[:match.start()] + title[match.end():]
    return title, part

def clean_title(title):
    # remove everything inside parenthesis
    title = re.sub('[([{].*?[)\]}]', '', title)
    # replace dots, underscores and dashes with spaces
    title = re.sub('[\._\-\'"]', ' ', title)
    stitle = title.split()
    title = []
    # loop on name
    for word in stitle:
        is_not_a_blackword = True
        for blackword in blackwords:
            if word.lower() == blackword.lower():
                is_not_a_blackword = False
                break
        if is_not_a_blackword:
            title.append(word)
        else:
            break
    title = ' '.join(title)
    return title

