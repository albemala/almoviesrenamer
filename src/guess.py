import datetime
import re

import utils
from movie import Movie

# black words in file names
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
    'DEiTY', 'FLAiTE', 'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS',
    'UnSeeN', 'aXXo', 'KLAXXON', 'NoTV', 'ZeaL', 'LOL'
]


def guess_info(title):
    """
    given a title, tries to guess as much information as possible.

    guessed information:
    title, year, language, part
    """

    # create info dictionary
    info = dict()
    # guess year
    title, year = guess_year_(title)
    if year != None:
        info.update({Movie.YEAR: year})
    # guess language
    title, language = guess_language_(title)
    if language != None:
        info.update({Movie.LANGUAGE: language})
    # guess part
    title, part = guess_part_(title)
    if part != None:
        info.update({Movie.PART: part})
    # guess subtitles
    title, subtitles = guess_subtitles_(title)
    if subtitles != None:
        info.update({Movie.SUBTITLES: subtitles})
    # clean title
    title = clean_title_(title)
    info.update({Movie.TITLE: title})
    # return guessed information
    return info


def guess_year_(title):
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


def guess_language_(title):
    """
    guess movie language, looking for ISO language representation in title
    """

    language = None
    match = re.search(r'\b([a-zA-Z]{3})\b', title)
    if match:
        # get corresponding language, given 3-letters ISO language code found
        language = utils.alpha3_to_language(match.group(0))
        # language detected
        if language != None:
            # remove language from title
            title = title[:match.start()] + title[match.end():]
    return title, language


def guess_subtitles_(title):
    """
    guess subtitles subtitles, looking for ISO subtitles representation in title
    """

    subtitles = None
    match = re.search(r'(?:[^a-zA-Z0-9]sub )([a-zA-Z]{3})(?:[^a-zA-Z0-9])', title)
    if match:
        # get corresponding subtitles, given 3-letters ISO subtitles code found
        subtitles = utils.alpha3_to_language(match.group(1))
        # subtitles detected
        if subtitles != None:
            # remove subtitles from title
            title = title[:match.start() + 1] + title[match.end() - 1:]
    return title, subtitles


def guess_part_(title):
    """
    guess movie part, e.g. CD1 -> 1
    """

    part = None
    # search part, which can be like, for example, disk1 or disk 1
    match = re.search(r'(?:cd|disk|part[ ]?)(\d)', title, re.IGNORECASE)
    if match:
        # get part number
        part = match.group(1)
        # remove part from title
        title = title[:match.start()] + title[match.end():]
    return title, part


def clean_title_(title):
    # remove everything inside parenthesis
    title = re.sub('[([{].*?[)\]}]', ' ', title)
    # replace dots, underscores and dashes with spaces
    title = re.sub(r'[._-]', ' ', title)
    stitle = title.split()
    title = []
    # loop on name
    # keep only words which are not black words
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
