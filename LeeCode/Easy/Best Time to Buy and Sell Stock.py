class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        min_price=float("inf")#先讓最小值極大化
        max_profit=0
        for p in prices:
            if p < min_price: #當比最小值小更新最小值
                min_price=p
            elif p-min_price>max_profit: #更新最大利潤
                max_profit=p-min_price

        return max_profit
        
        
prices = [7,1,5,3,6,4]
sol=Solution()
print(sol.maxProfit(prices))