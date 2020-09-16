# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:04:57 2020

@author: miame
"""

# =============================================================================
# Assignment description:
# =============================================================================

"""
A Singly Linked List is a list comprised of many nodes. Each node contains
some data, in our case just an integer, and a pointer to the next node in the list.
The first node in the list is known as the head node. The last node in the graph
has a pointer to a null next item.

For each of the required methods, figure out what the computation complexity
of your implementation is and state whether or not you think that is the best
possible complexity class. Make sure that your implementation is correct and
robust to bad inputs.

You are free to define whatever private helper functions/classes/etc. that you
need, but make sure that your implementation has the above public facing
interface. You may NOT use any other data structures to implement this. That
means no Lists, Arrays, Tuples, etc. You should use the following as the starter
definition for a Node class:

"""

# starter code from assignment:

class Node:
    def __init__(self, _value=None, _next=None):
        self.value = _value
        self.next = _next
    def __str__(self):
        return str(self.value)

# =============================================================================
# defining class LinkedList
# =============================================================================

class LinkedList():

    def __init__(self, value):
        # Takes a number and sets it as the value at the head of the List
        # 2 moves
        # best possible complexity class
        self.value = value
        self.count = 1 #initializing counter for the list length

    def length(self):
        # Returns the length of the list
        # returns current value of tracker
        # when counting previous moves to add to counter, approximately n moves (more if removed nodes)
        # best possible complexity class
        return self.count

    def addNode(self, new_value):
        # Takes a number and adds it to the end of the list
        # searches for end of the list (n-1 moves), then adds node (1 move)
        # total n moves
        # best possible complexity class
        if type(new_value) == int:
            new_node = Node(new_value)
            current_node = self.value
            while current_node.next != None: #iterating over until end of the list; list ends in None
                current_node = current_node.next
            current_node.next = new_node #adding new node
            self.count += 1
        else:
            print("Error: new_value must be an integer.")

    def addNodeAfter(self, new_value, after_node):
        # Takes a number and adds it after the 'after_node'
        # calls Node function, where args _value = new_value and _next = after_node
        # updates after_node.next
        # takes up to n  moves
        # best possible complexity class
        if type(new_value) == int :
            new_node = Node(new_value, after_node.next)
            after_node.next = new_node
            self.count += 1
        else:
            print("Error. Check that new_value is an integer.")

    def addNodeBefore(self, new_value, before_node):
        # Takes a value and adds before the before_node
        # iterates over list until 'next' = 'before_node' then calls addNodeAfter'
        # takes up to n-1 moves to find before node, and n moves to add node
        # total complexity: 2n-1
        # best possible complexity class
        current_node = self.value
        while current_node.next != before_node:
            current_node = current_node.next
        return self.addNodeAfter(new_value, current_node)
        # NB: length counter updated in 'addNodeAfter'

    def removeNode(self, node_to_remove):
        # Removes a node from the list
        # iterates over list until the next node == node_to_remove, then replaces the next node
        # like adding a node: takes n-1 moves to find node to remove, then 1 move to remove
        # total complexity: n moves
        # best possible complexity class
        current_node = self.value
        while current_node.next != node_to_remove:
            current_node = current_node.next
        current_node.next = node_to_remove.next
        self.count -= 1 #

    def removeNodesByValue(self, value):
        # Takes a value, removes all nodes with that value
        # iterates over list checking if values match
        # takes n moves to iterate over list, and n moves for each call removeNode
        # so if only one instance in the list, complexity is n*n = n^2
        # probably could be less complex, but not sure how
        current_node = self.value
        while current_node != None: # for all elements in the list
            if current_node.value == value:
                self.removeNode(current_node)
            current_node = current_node.next

    def reverse(self):
        # Reverses the order of the linked list
        # think of changing the "arrows" from one node to another, not swapping elements
        # iterates to the end of the list, changing the arrow at each step
        # requires n moves to iterate over, one arrow change per iteration plus final change
        # total complexity: 2n + 1
        # best possible complexity class
        current_node = self.value #starts at first node
        previous_node = None # because it's first, nothing previous
        while current_node != None: #when done, current node will be at the end of the list, which is None
            next_node = current_node.next #initialize next node in list
            current_node.next = previous_node # reversing the arrow
            previous_node = current_node
            current_node = next_node # moving up one
        self.value = previous_node # lastly, change the first node

    def __str__(self):
        # Displays the list in some reasonable way
        printer = ""
        current_node = self.value
        while current_node.next != None: # iterates until the second to last node
            printer += str(current_node.value) + ', '
            current_node = current_node.next
        printer += str(current_node.value) #last node has no comma
        return "Nodes: " + printer

    # helper function
    def findNodeByValue(self, value):
        current_node = self.value
        while current_node != None:
            if current_node.value == value:
                return current_node
            else:
                current_node = current_node.next




# =============================================================================
# Testing
# =============================================================================

# creating some nodes
node_a = Node(9)

# initializing with node_a as the first node
ll = LinkedList(node_a)
print(ll)

# testing the length
ll.length()

# adding nodes
#ll.addNode(node_a) #correct errors
ll.addNode(8)
ll.addNode(7)

# testing print
print(ll)

# testing length
ll.length()

# testing addNodeAfter
ll.addNodeAfter(52, ll.findNodeByValue(8))
ll.addNodeAfter(52, ll.findNodeByValue(9))
print(ll)

# testing addNodeBefore

ll.addNodeBefore(75, ll.findNodeByValue(8))
print(ll)

# testing removeNode()
ll.removeNode(ll.findNodeByValue(75))
print(ll)

# testing removeNodesByValue()

ll.removeNodesByValue(52)
print(ll)

## reverse()
print(ll)
ll.reverse()
print(ll)
