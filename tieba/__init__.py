import re
pattern = re.compile(r'(http|ftp|https)+:\/\/[\w\-_]+(?:\.[\w\-_]+)([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
# pattern = re.compile(r'[a-zA-z]+://[^\s\-_]*')
result = pattern.findall('http://www.baifjf.com.cn')
print(result)
