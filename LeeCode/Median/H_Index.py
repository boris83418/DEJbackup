class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """
        sortedlist=sorted(citations,reverse=True)
        hindex=0
        for i, v in enumerate(sortedlist):
            #當目前引用次數V大於目前的ranking，hindex變成現在的ranking
            if v>=i+1:
                hindex=i+1
            #如果沒超過代表越來越少
            else:
                break
                
        return hindex
        




citation1=[6,5,0,1,3]   
citation2=[3,1,1]

sol=Solution()
print(sol.hIndex(citation1))   
   