#跳到最後一格或是超過最後一格都是贏家
class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        thelastlocation=len(nums)-1 #最後要跳到的位置 #4
        for i in range(thelastlocation,-1,-1): #從後面慢慢往前推
            if i+nums[i]>=thelastlocation:  #當前一個點可以到下一個點，代表路是通的可以更新最終點
                thelastlocation=i
        return thelastlocation==0 #跳回到原點


       

nums0 = [2,3,1,1,5]
nums1 = [3,2,1,0,5]
nums2 = [1,2]
nums3 = [0]
sol=Solution()
print(sol.canJump(nums0))#true
print(sol.canJump(nums1))#false
print(sol.canJump(nums2))#true
print(sol.canJump(nums3))#true
