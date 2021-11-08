#coding=utf-8
class Graph(object):
    def __init__(self, mat):
        self.mat = mat
        self.nodenum = self.get_nodenum()
        self.edgenum = self.get_edgenum()
 
    def get_nodenum(self):
        return len(self.mat)
 
    def get_edgenum(self):
        count = 0
        for i in range(self.nodenum):
            for j in range(i):
                if self.mat[i][j] > 0 and self.mat[i][j] < float('inf'):
                    count += 1
        return count
 
    def kruskal(self):
        res = []
        if self.nodenum <= 0 or self.edgenum < self.nodenum-1:
            return res
        edge_list = []
        for i in range(self.nodenum):
            for j in range(i,self.nodenum):
                if self.mat[i][j] < float('inf'):
                    edge_list.append([i, j, self.mat[i][j]])#按[begin, end, weight]形式加入
        edge_list.sort(key=lambda a:a[2])#已经排好序的边集合
        
        group = [[i] for i in range(self.nodenum)]
        for edge in edge_list:
            for i in range(len(group)):
                if edge[0] in group[i]:
                    m = i
                if edge[1] in group[i]:
                    n = i
            if m != n:
                res.append(edge)
                group[m] = group[m] + group[n]
                group[n] = []
        return res
 
    def prim(self):
        res = []
        if self.nodenum <= 0 or self.edgenum < self.nodenum-1:
            return res
        res = []
        seleted_node = [0]
        candidate_node = [i for i in range(1, self.nodenum)]
        
        while len(candidate_node) > 0:
            begin, end, minweight = 0, 0, float('inf')
            for i in seleted_node:
                for j in candidate_node:
                    if self.mat[i][j] < minweight:
                        minweight = self.mat[i][j]
                        begin = i
                        end = j
            res.append([begin, end, minweight])
            seleted_node.append(end)
            candidate_node.remove(end)
        return res
