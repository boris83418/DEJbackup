#去超過兩個以上的元素

class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        current_position=0
        count=1
        list=[]

        while current_position <len(nums):
            if current_position==0:
                # print("test")
                # print("現在位置",current_position)
                # print("現在位置的數字",nums[current_position])
                # print("出現幾次",count)
                current_position+=1
            elif nums[current_position]==nums[current_position-1]:
                # print("test1")
                count+=1
                # print("現在位置",current_position)
                # print("現在位置的數字",nums[current_position])
                # print("出現幾次",count)
                if count>2:
                    list.append(current_position)
                    # print("重複兩次以上的位置",list)  
                current_position+=1
            else:
                # print("test2")
                count=1
                # print("現在位置",current_position)
                # print("現在位置的數字",nums[current_position])
                # print("出現幾次",count)
                current_position+=1
        for i in list:
            nums[i]=None

        nums.sort(key=lambda x:(x is None))
        k = len([num for num in nums if num is not None])
        return(k)
nums=[0,0,1,1,1,1,2,3,3]
current_position=0
count=1
list=[]
sol=Solution()
k=sol.removeDuplicates(nums)
print("修改後的陣列",nums)
print("剩餘的元素",k)