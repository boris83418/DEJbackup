class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        maxprofit=0
        #把每一部分profit慢慢加起來
        for i in range(len(prices)-1):
            if prices[i]<prices[i+1]:
                maxprofit+=prices[i+1]-prices[i]
                
        return maxprofit
        
Sol=Solution()
prices = [7,1,5,3,6,4]
print(Sol.maxProfit(prices))
