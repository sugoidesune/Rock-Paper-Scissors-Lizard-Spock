import dateparser
import re#

date= str(dateparser.parse('morgen in einer woche'))

#re.sub("-","",date[:10])

print "http://tv.orf.at/program/orf1/"+re.sub("-","",date[:10])
