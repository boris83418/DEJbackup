import random
class RandomizedSet(object):

    def __init__(self):
        self.list=[]
    def insert(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val not in self.list:
            self.list.append(val)
            return True
        return False


    def remove(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val in self.list:
            self.list.remove(val)
            return True
        return False

    def getRandom(self):
        """
        :rtype: int
        """
        return random.choice(self.list)



# 測試用例
obj = RandomizedSet()
print(obj.insert(0))  
print(obj.remove(2))  
print(obj.insert(2))  
print(obj.getRandom())  
print(obj.remove(1))  
print(obj.insert(2)) 
print(obj.getRandom()) 




### Chatgpt寫法
# import random

# class RandomizedSet(object):

#     def __init__(self):
#         # 存儲元素的列表
#         self.list = []
#         # 存儲值到索引的映射
#         self.dict = {}

#     def insert(self, val):
#         """
#         :type val: int
#         :rtype: bool
#         """
#         # 如果元素已存在，返回 False
#         if val in self.dict:
#             return False
#         # 如果元素不存在，將它添加到列表末尾，並在哈希表中記錄索引
#         self.dict[val] = len(self.list)
#         self.list.append(val)
#         return True

#     def remove(self, val):
#         """
#         :type val: int
#         :rtype: bool
#         """
#         # 如果元素不在哈希表中，無法移除，返回 False
#         if val not in self.dict:
#             return False
#         # 獲取要移除的元素的索引
#         idx_to_remove = self.dict[val]
#         # 將最後一個元素與要移除的元素交換
#         last_element = self.list[-1]
#         self.list[idx_to_remove] = last_element
#         self.dict[last_element] = idx_to_remove
#         # 移除最後一個元素
#         self.list.pop()
#         del self.dict[val]
#         return True

#     def getRandom(self):
#         """
#         :rtype: int
#         """
#         # 從列表中隨機選擇一個元素
#         return random.choice(self.list)
