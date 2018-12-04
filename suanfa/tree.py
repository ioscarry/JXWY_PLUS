class Node(object):
    '''节点类,3个参数, 其中elem为本身的值.'''
    def __init__(self,elem=-1,lchild=None,rchild=None):
        self.elem = elem
        self.lchild = lchild
        self.rchild = rchild

class Tree(object):
    '''树类'''
    def __init__(self,root=None):
        self.root = root

    def add(self,elem):
        '''为树添加节点'''
        node = Node(elem)
        # 如果是空的,则对根节点赋值
        if self.root == None:
            self.root = node
        else:
            queue = []
            queue.append(self.root)
            # 对已有节点进行遍历
            while queue:
                # 弹出队列的第一个元素
                cur = queue.pop(0)
                if cur.lchild == None:
                    cur.lchild = node
                    return
                elif cur.rchild == None:
                    cur.rchild = node
                    return
                else:
                    # 若左右子树都不为空,加入队列继续判断
                    queue.append(cur.lchild)
                    queue.append(cur.rchild)
                    
            # 最终结果是先从左开始查, 如果有空位就插入元素.