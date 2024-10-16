class Solution(object):
    def jump(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        jump=0
        current_end=0 #當前跳到最遠的位置
        farthest=0 #可達到最遠位置
        for i in range(len(nums)-1):#跳轉到最後一個元素前的位置
            farthest=max(farthest,i+nums[i])
            #如果剛好一步到位或超過位置，就結束
            if current_end>=len(nums)-1:
                break
            if i==current_end:#剛好等於邊界位置
                jump+=1#還需要跳一步
                current_end=farthest
        return jump 
                
 
            
nums1 = [2,3,1,1,4]
nums2 = [2,3,0,1,4]
nums3=[3,4,3,2,5,4,3]
nums4=[4,1,1,3,1,1,1]
nums5=[10,9,8,7,6,5,4,3,2,1,1,0]
sol=Solution()
print(sol.jump(nums1))        
print(sol.jump(nums2))        
print(sol.jump(nums3))        
print(sol.jump(nums4))        
print(sol.jump(nums5))        
     
