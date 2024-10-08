class Solution(object):
    def removeElement(self, nums, val):
        i=0
        while i<len(nums):
            if nums[i]==val:
                nums.pop(i)
            else:
                i+=1
        return len(nums)
                
sol=Solution()
nums = [3,2,2,3]
val = 3
k=sol.removeElement(nums,val)
print("修改後的陣列",nums)
print("剩餘的元素",k)

