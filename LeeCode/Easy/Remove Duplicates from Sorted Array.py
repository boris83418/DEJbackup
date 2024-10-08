#去重
class Solution(object):
    def removeDuplicates(self, nums):
        i=0
        while i<len(nums)-1:
            if nums[i]==nums[i+1]:
                nums.remove(nums[i+1])
            else:
                i+=1
        return len(nums)
sol=Solution()
nums = [1,1,2]
k=sol.removeDuplicates(nums)
print("修改後的陣列",nums)
print("剩餘的元素",k)


