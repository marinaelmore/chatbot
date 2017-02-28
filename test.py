import re


titles2 = []
movie = 'Toy Story (1995)'
title_regex = '(.+)(?:,\w+)?\s\(\d{4}\)'

title = re.findall(title_regex, movie)
title2 = title[0]
title2 = title2.replace(", The", "").replace(", An", "").replace(", A", "")
titles2.append(title2)

print titles2