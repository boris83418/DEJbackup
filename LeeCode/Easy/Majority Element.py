#找眾數
#眾數定義：在一個數組中，眾數是出現次數超過 n/2 的元素（其中 n 是數組的長度）。
#因此，即使數組中的其他元素的出現次數小於或等於 n/2，眾數出現的次數也保證會讓它在排序後的中間位置。
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums.sort()
        return nums[len(nums)//2]
        
        
sol=Solution()
print(sol.majorityElement([3,2,3]))
