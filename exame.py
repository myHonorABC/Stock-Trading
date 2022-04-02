# 对格式化后的合法工号，去重后，按照字典序升序输出
# @param employeeIdList string字符串一维数组 待整理工号的列表
# @return string字符串一维数组
#
class Solution:
    def process(self, X, Y):
        # write code here
        x = X.split(' ')
        x = list(set(x))
        y = Y.split(' ')
        y = list(set(y))
        result = []
        for c in x:
            if (c in y):
                result.append(c)
        return ' '.join(sorted(result, key=lambda x:x[0]))


if __name__ == '__main__':
    s = Solution()
    result = s.process('a b d g f c d1', 'g d e e1 a1')
    print(result)