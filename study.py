class FourCal:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def setdata(self, first, second):
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result
    def mul(self):
        result = self.first * self.second
        return result
    def sub(self):
        result = self.first - self.second
        return result
    def div(self):
        result = self.first / self.second
        return result

a = FourCal()
a.setdata(4, 2)
print(a.first)
print(a.second)
print(a.add())
print(a.mul())
print(a.sub())
print(a.div())


'''
#jump2python Q4-7

f = open("test.txt", 'r')
read_all = f.read()
f.close()
read_rev = read_all.replace("java", "python")

f = open("test_rev.txt", 'w')
f.write(read_rev)
f.close()
'''

'''
#jump2python Q4-6
line = input("아무거나 입력해 주세요: ")
f = open("test.txt", 'a')
f.write(line)
f.write("\n")
f.close()
'''

'''
#jump2python Q4-2
def average_cal(*args):
    result = 0
    for i in args:
        result += i
    print(result/len(args))

average_cal(3,4,5,6)
average_cal(12.432,432431.12412,5235.23)
'''

'''
#jump2python Q4-2
def average_cal():
    numbers = [0]
    while True:
        answer = int(input("숫자를 입력하세요: "))
        if answer == 0:
            break
        numbers.append(answer)

    total = 0
    for i in numbers:
        total += i
    average = total/len(numbers)
    print("평균: %d" %average)

average_cal()
'''

'''
#jump2python Q4-1
def is_odd():
    while True:
        data = int(input("숫자를 입력하세요: "))
        if data == 0:
            break
        data = data%2
        if data == 0:
            print("짝수 입니다.")
        else:
            print("홀수 입니다.")
is_odd()
'''

'''
#sys2.py
import sys
args = sys.argv[1:]
for i in args:
    print(i.upper(), end=' ')
print('')
'''

'''
# adddata.py
f = open("새파일.txt", 'a')
for i in range(11, 20):
    data = "%d번째 줄입니다. \n" %i
    f.write(data)
f.close()
'''

'''
# readline_all.py
f = open("새파일.txt", 'r')
while True:
    line = f.readline()
    if not line: break
    print(line)
f.close()
'''

'''
# readline_test.py
f = open("새파일.txt", 'r')
line = f.readline()
print(line)
f.close()
'''

'''
# writedata.py
f = open("새파일.txt", 'w')
for i in range(1,11):
    data = "%d번째 줄입니다. \n" %i
    f.write(data)
f.close()
'''

'''
#jump2python Q3-6
numbers = [1, 2, 3, 4, 5]
print([2*a for a in numbers if a % 2 == 1])
'''

'''
#jump2python Q3-5

marks = [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]

sum_of_a=0
for a in marks:
    sum_of_a += a

print(sum_of_a/len(marks))
'''

'''
#jump2python Q3-4

for a in range(0,100):
    print(a+1)
'''

'''
#jump2python Q3-3

star = '*'
number = 0
while number < 5:
    number += 1
    print(star*number)
'''

'''
#jump2python Q3-2

a=0
sum_of_a=0

while a<1000:
    a += 1
    if a % 3 == 0:
        sum_of_a += a
print(sum_of_a)
'''

'''
#marks1.py

marks = [90, 25, 67, 45, 80]

for res in marks:
    if res > 60:
        print('점수 %d점, 합격입니다.' %res)
    else:
        continue
'''

'''
# coffee.py
coffee = 10
while True:
    money = int(input("돈을 넣어 주세요: "))
    if money == 300:
        print("커피를 줍니다.")
        coffee -= 1

    elif money > 300:
        print("거스름돈 %d를 주고 커피를 줍니다." %(money-300))
        coffee -=1
    else:
        print("돈을 다시 돌려주고 커피를 주지 않습니다.")
        print("남은 커피의 양은 %d개 입니다." %coffee)
    if coffee == 0:
        print("커피가 다 떨어졌습니다. 판매를 중지합니다.")
        break
'''

