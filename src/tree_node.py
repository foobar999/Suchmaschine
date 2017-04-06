
#===============================================================================
# class TreeNode(object):
# 
#     def __init__(self, parent = None, key = None):
#         self.key = key
#         self.parent = parent
#         self.childs = []
# 
#     
#     def preorder(self, depth = 0):
#         #return 'TreeNode(key=' + str(self.key) + ' childs=' + str(self.childs) + ')'
#         res = ' ' * depth + str(self.key)
#         for child in self.childs:
#             res += '\n' + child.preorder(depth + 2)
#         return res
#     
#      
#     def __repr__(self):
#         #return 'TreeNode(key=' + str(self.key) + ' childs=' + str(self.childs) + ')'
#         return self.preorder()
#===============================================================================
