import re

print(re.findall(r"a(.*)b(c)","a\nbc",re.DOTALL))