import re

movie = 'Usual Suspects, The (1995)'
title_regex = '(.+)(?:,\w+)?\s\(\d{4}\)'
print re.findall(title_regex, movie)