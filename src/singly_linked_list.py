from platform import node

class Node(object):
 
    def __init__(self, data, next):
        self.data = data
        self.next = next
 
 
class SingleList(object):
 
    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0
 
    def __str__(self):
        current_node = self.head
        fullListString = "["
        while current_node is not None:
            fullListString = fullListString + str(current_node.data) + "->"
            current_node = current_node.next
        fullListString = fullListString + "None]"
        return fullListString
 
    def __iter__(self):
        return SingleListIter(self.head)
    
    def __len__(self):
        return self.len
    
    def append(self, data):
        node = Node(data, None)
        if self.head is None:   # first element in empty list
            self.head = self.tail = node
            self.len += 1
        else:   # add element to existing list
            currentNode = self.head
            lastNode = None
#            while currentNode != None:
            while True:
                
                if currentNode is None  :           # insert as last element
                    lastNode.next = node
                    self.tail = node
                    self.len += 1
                    break
                    
                elif currentNode.data < node.data:  # continue the loop
                    lastNode = currentNode
                    currentNode = currentNode.next
                    continue
                    
                elif currentNode.data == node.data: # value is already in the list
                    break
                
                elif currentNode.data > node.data:
                    if lastNode == None:            # insert as first element
                        self.head = node
                        node.next = currentNode
                    else:                           # insert inside the list
                        lastNode.next = node
                        node.next = currentNode
                    self.len += 1
                    break
                    
                lastNode = currentNode
                currentNode = currentNode.next
            '''
            while currentNode.data < node.data: # until currentNode is equal or greater than the new node
                currentNode = currentNode.next
            if currentNode.data == node.data:
                print("Don't add the node.")
            else:   # currentNode > new node
                
            self.len += 1
            self.tail.next = node
        self.tail = node
        '''


    def remove(self, node_value):
        current_node = self.head
        previous_node = None
        while current_node is not None:
            if current_node.data == node_value:
                # if this is the first node (head)
                if previous_node is not None:
                    previous_node.next = current_node.next
                else:
                    self.head = current_node.next
 
            # needed for the next iteration
            previous_node = current_node
            current_node = current_node.next




class SingleListIter(object):

    def __init__(self, node):
        self.node = node
 
    def __next__(self):
        if self.node == None:
            raise StopIteration()
        else:
            data = self.node.data
            self.node = self.node.next
            return data