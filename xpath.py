from lxml import etree

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
     </ul>
 </div>
'''
# 利用etree.HTML, 将字符串解析为HTML文档
html = etree.HTML(text)

# 按字符串序列化HTML文档
result = etree.tostring(html)
print(type(html))
print(type(result))
print(result)

html2 = etree.parse('hello.html')
result2 = etree.tostring(html2,pretty_print=True)

print(result2)

print('-------------------')
result3 = html2.xpath('//li') # 获取所有li标签
print(result3)

result4 = html2.xpath('//li/@class')  # 获取li标签的所有class属性
print(result4)

result5 = html2.xpath('//li/a[@href="link1.html"]') # 获取li标签下href属性值为link1.html的a标签
print(result5)

result6 = html2.xpath('//li//span')
print(result6)

result7 = html2.xpath('//li/a//@class')
print(result7)

result8 = html2.xpath('//li[last()]/a/@href') # 获取最后一个li标签下a标签的href属性
print(result8)

result9 = html2.xpath('//li[last()-1]/a/text()') # 获取倒数第二个元素的内容
print(result9)
result10 = html2.xpath('//li[last()-1]/a')
print(result10[0].text)

result11 = html2.xpath('//*[@class="bold"]') # 获取class="bold"的标签
print(result11[0].tag)