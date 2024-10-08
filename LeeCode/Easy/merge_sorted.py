###merge兩個排序好的list

class Solution:
    def merge(self, nums1, m, nums2, n):
        i,j,k=m-1,n-1,m+n-1
        #當i跟j都有數字的時候
        while i>=0 and j>=0:
            #如果nums1的數字比nums2的數字大，就把nums1的數字放到nums1的最後面
            if nums1[i]>nums2[j]:
                nums1[k]=nums1[i]
                i-=1
            #如果nums2的數字比nums1的數字大，就把nums2的數字放到nums1的最後面
            else:
                nums1[k]=nums2[j]
                j-=1
            k-=1
        #如果nums1還有剩餘的數字，則不需要處理，因為它們已經在正確的位置
        #如果nums2的數字比nums1的數字大，就把nums2的數字放到nums1的最後面
        while j>=0:
            nums1[k]=nums2[j]
            k-=1
            j-=1
            
#創建類的實例
solution1=Solution()
nums1=[1,2,3,0,0,0]
m=3
nums2=[2,5,6]
n=3
solution1.merge(nums1,m,nums2,n)
print(nums1)
    
solution2=Solution()
nums1=[1]
m=1
nums2=[]
n=0
solution2.merge(nums1,m,nums2,n)
print(nums1)

solution3=Solution()
nums1=[0]
m=0
nums2=[1]
n=1
solution3.merge(nums1,m,nums2,n)
print(nums1)