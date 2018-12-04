class SingleNode(object):
    '''单向循环链表的结点'''
    def __init__(self,item):
        # item存放数据元素
        self.item = item
        # next是下一个节点的标识
        self.next = None
        # 定义cur为游标指针

class SinCycLinkList(object):
    '''单链表'''
    def __init__(self):
        # 初始值默认None
        self.__head = None

    def is_empty(self):
        '''判断链表是否为空'''
        return self.__head == None

    def length(self):
        '''链表长度'''
        if self.is_empty():
            return 0
        else:
            # cur初始时指向头节点
            cur = self.__head
            count = 0
            # 尾节点指向None,当未到达尾部时
            while cur.next != self.__head:
                count += 1
                # 移动游标
                cur = cur.next
            # 循环结束累加, 此时累加的是最后一个节点的计数
            count += 1
            return count

    def travel(self):
        '''遍历链表'''
        cur = self.__head
        while cur.next != self.__head:
            print(cur.item,end=' ')
            cur = cur.next
        # 打印最后一个节点的数据
        print(cur.item)

    def add(self, item):
        '''头部添加元素'''
        node = SingleNode(item)
        if self.is_empty():
            self.__head = node
            # 将第一个节点的next指向节点, 形成循环链表
            node.next = self.__head
        else:
            # 创建游标, 用于找到尾节点
            cur = self.__head
            # 循环遍历找到尾节点
            while cur.next is not self.__head:
                cur = cur.next
            node.next = self.__head
            self.__head = node
            cur.next = self.__head


    def append(self,item):
        '''尾部添加元素'''
        node = SingleNode(item)
        # 判断链表是否为空
        if self.is_empty():
            self.__head = node
            node.next = self.__head
        # 若不为空,则找到尾部,将尾节点的next指向新节点
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            # 尾部添加新节点
            cur.next = node
            # 新节点与头部链接形成循环
            node.next = self.__head

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
            # 设置前驱游标, 默认为None
            pre = None
            while cur.next is not self.__head:
                if cur.item == item:

                    # 1. 若删除的节点为头节点
                    if cur == self.__head:
                        # 定义尾节点游标,找到尾节点
                        rear = self.__head
                        while rear.next is not self.__head:
                            rear = rear.next
                        # 将头节点指向头节点的后续节点
                        self.__head = cur.next
                        rear.next = self.__head
                    else:
                        # 待删除节点在链表中部和尾部的时候
                        pre.next = cur.next
                    return
                else:
                    pre = cur
                    cur = cur.next
            if cur.item == item:
                if cur == self.__head:
                    # 只有一个节点, 并且该节点就是要删除的节点
                    self.__head = None
                else:
                    # 多个节点,尾节点符合删除条件
                    pre.next = self.__head


    def search(self,item):
        cur = self.__head

        while cur is not self.__head:
            if cur.item == item:
                return True
            else:
                cur = cur.next
        if cur.item == item:
            return True
        else:
            return False


if __name__ == '__main__':
    ll = SinCycLinkList()
    print(ll.length())
    ll.add(1)
    ll.add(22)
    ll.append(33)
    ll.travel()
    print(ll.search(44))
    print(ll.search(33))
    ll.insert(-4,88)
    ll.travel()