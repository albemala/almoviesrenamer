# -*- coding: latin-1 -*-

from xml.dom import minidom

__author__ = "Alberto Malagoli"

# program name and version, used in excepthook
PROGRAM_NAME = "ALmoviesRenamer"
PROGRAM_VERSION = "3.0"

class Data(object):

    def __init__(self, element, **kw):
        self._element = element
        for key, value in kw.items():
            setattr(self, key, value)

class Database(object):

    # Override those names in sub-classes for specific ISO database.
    field_map = dict()
    data_class_base = Data
    data_class_name = None
    xml_tag = None
    no_index = []

    def __init__(self, filename):
        self.objects = []
        self.indices = {}

        self.data_class = type(self.data_class_name, (self.data_class_base,), {})

        f = open(filename, 'rb')

        tree = minidom.parse(f)

        for entry in tree.getElementsByTagName(self.xml_tag):
            mapped_data = {}
            for key in entry.attributes.keys():
                mapped_data[self.field_map[key]] = (
                    entry.attributes.get(key).value)
            entry_obj = self.data_class(entry, **mapped_data)
            self.objects.append(entry_obj)

        # Construct list of indices: primary single-column indices
        indices = []
        for key in self.field_map.values():
            if key in self.no_index:
                continue
            # Slightly horrible hack: to evaluate `key` at definition time of
            # the lambda I pass it as a keyword argument.
            getter = lambda x, key = key: getattr(x, key, None)
            indices.append((key, getter))

        # Create indices
        for name, _ in indices:
            self.indices[name] = {}

        # Update indices
        for obj in self.objects:
            for name, rule in indices:
                value = rule(obj)
                if value is None:
                    continue
                if value in self.indices[name]:
                    print(
                        '{0} {1} already taken in index {2} and will be '
                        'ignored. This is an error in the XML databases.'.format
                        (self.data_class_name, value, name))
                self.indices[name][value] = obj

    def __iter__(self):
        return iter(self.objects)

    def __len__(self):
        return len(self.objects)

    def get(self, **kw):
        assert len(kw) == 1, 'Only one criteria may be given.'
        field, value = kw.items()[0]
        return self.indices[field][value]

class Languages(Database):
    """Provides access to an ISO 639-1/2 database (Languages)."""

    field_map = dict(iso_639_2B_code = 'bibliographic',
                     iso_639_2T_code = 'terminology',
                     iso_639_1_code = 'alpha2',
                     name = 'name')
    data_class_name = 'Language'
    xml_tag = 'iso_639_entry'

def load_languages_db():
    global languages_db
    languages_db = Languages('languages.xml')

def load_country_to_languages_db():
    global country_to_languages_db
    country_to_languages_db = dict()
    with open('countries_languages_2') as f:
        for line in f:
            country, language = line.strip('\n').split('|')
            country_to_languages_db.update({country: language})

def countryToLanguage(given_country):

    return country_to_languages_db[given_country]

