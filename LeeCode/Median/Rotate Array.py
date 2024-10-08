#調整list內中的順序
class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """     
        """
        假設你的列表 nums 長度為 7，即 n = 7。
        如果 k 是 10，這意味著你希望將列表向右旋轉 10 次。但實際上，旋轉 10 次與旋轉 3 次（因為 10 - 7 = 3）是等效的。
        因此，進行多於 n 次的旋轉是沒有必要的。
        """
        n=len(nums)
        k=k%n
        print(k)
        #切片將後面元素往前面放然後取代原本list
        nums[:]=nums[-k:]+nums[:-k]  
        return nums

sol=Solution()
print(sol.rotate([1,2,3,4,5,6,7],3))
print(sol.rotate([-1,100,3,99],2))

