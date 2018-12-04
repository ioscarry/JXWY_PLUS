class SingleNode(object):
    '''单链表的结点'''
    def __init__(self,item):
        # item存放数据元素
        self.item = item
        # next是下一个节点的标识
        self.next = None
        # 定义cur为游标指针

class SingleLinkList(object):
    '''单链表'''
    def __init__(self):
        # 初始值默认None
        self.__head = None

    def is_empty(self):
        '''判断链表是否为空'''
        return self.__head == None

    def length(self):
        '''链表长度'''
        # cur初始时指向头节点
        cur = self.__head
        count = 0
        # 尾节点指向None,当未到达尾部时
        while cur != None:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        '''遍历链表'''
        cur = self.__head
        while cur != None:
            print(cur.item,end=' ')
            cur = cur.next
        print('')

    def add(self, item):
        '''头部添加元素'''
        node = SingleNode(item)
        if self.is_empty():
            self.__head = node
        else:
            node.next = self.__head
            self.__head = node


    def append(self,item):
        '''尾部添加元素'''
        node = SingleNode(item)
        # 判断链表是否为空
        if self.is_empty():
            self.__head = node
        # 若不为空,则找到尾部,将尾节点的next指向新节点
        else:
            cur = self.__head
            while cur.next != None:
                cur = cur.next
            cur.next = node

    def insert(self,pos,item):
        '''指定位置添加元素'''
        # 若指定位置pos为第一个元素之前，则执行头部插入
        if pos <= 0:
            self.add(item)
            # 若指定位置超过链表尾部，则执行尾部插入
        elif pos > (self.length()-1):
            self.append(item)
        # 找到指定位置
        else:
            node = SingleNode(item)
            count = 0
            cur = self.__head
            # 使游标定位到pos的前一个位置, 然后在这个位置的next链接上新插入的节点
            while count < (pos-1):
                count += 1
                cur = cur.next
            node.next = cur.next
            cur.next = node

    def remove(self,item):
        '''删除节点'''
        if self.is_empty():
            return
        else:
            cur = self.__head
            # 还需设置个前驱游标,默认为None
            pre = None
            while cur is not None:
                if cur.item == item:
                    if cur == self.__head:
                        self.__head = cur.next
                    else:
                        # 待删除节点在链表中部和尾部的时候
                        pre.next = cur.next
                    break
                else:
                    pre = cur
                    cur = cur.next

    def search(self,item):
        cur = self.__head

        while cur is not None:
            if cur.item == item:
                return True
            else:
                cur = cur.next
        return False


if __name__ == '__main__':
    ll = SingleLinkList()
    print(ll.length())
    ll.add(1)
    ll.add(22)
    ll.append(33)
    ll.travel()
    print(ll.search(44))
    print(ll.search(33))
    ll.insert(-4,88)
    ll.travel()