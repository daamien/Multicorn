from multicorn import ForeignDataWrapper
import urllib
from icalendar import Calendar, Event

class ICalFdw(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(ICalFdw, self).__init__(options, columns)
        self.url = options.get('url', None)
	self.columns = columns

    def execute(self, quals, columns):
	ical_file = urllib.urlopen(self.url).read()
	cal = Calendar.from_string(ical_file)
        for v in cal.walk('vevent'):
            e = Event(v)
	    line = {}
            for column_name in self.columns:
                line[column_name] = e.decoded(column_name)
            yield line
