# not 을 붙이면 반대를 뜻함
print(not (5<10))

print(5**3) # 5^3
print(5%3) #나머지
print(5//3) #몫

# print에서 comma 로 연결하면 str형태가 아니더라도 출력을 시켜줌
# 이 때 comma 는 가본적으로 빈칸으로 연결을 시키지만 print('Value is "', value, '"', sep = '') 로
# 빈칸을 없앨수도 있음
# + 를 사용하면 붙여서 출력함
# 아니면 그냥 formatting 을 사용하는게 편함

# 조건문에서 and 와 & 은 같은 기능을 함
# 조건문에서 or 와 | 는 같은 기능을 함

number = 0
number = number + 2 # number += 2 와 같은 의미

from random import *

jumin = "910222-1205412"
print("생년월일 : " + jumin[:6]) # 처음부터 6 직전까지
print("뒤 7자리 : " + jumin[-7:]) # -7부터 끝까지

python = "Python is Amazing and new"
index = python.index("n")
print(index)
for i in range(python.count("n")-1):
    index = python.index("n", index+1)
    print(index)

age = 20
color = """동해물과 백두산이
마르고 닳도록"""
print("나는 {}살이며, {}색을 좋아해요.".format(age, color))
#아래는 파이썬 3.6 이상부터 가능
print(f"나는 {age}살이며, {color}색을 좋아해요.") # 이 방법이  MCNP나 PHITS 인풋 만들 때 더 좋을 듯.

# \r : 커서를 맨 앞으로
# \b : 백스페이스 (한 글자 삭제)

test_url = "https://google.com"

my_url_index = test_url.find("/")
my_url_index +=2
my_url = test_url[my_url_index:]
my_url_index = my_url.find(".")
my_url = my_url[:my_url_index]
print(my_url)

password = my_url[:3] + str(len(my_url)) +  str(my_url.count("e")) + "!"
print("생성된 비밀번호 : ", password)

password = "{}{}{}{}".format(my_url[:3], len(my_url), my_url.count("e"), "!")
print("{} 의 비밀 번호는".format(test_url), password)

# list 관련 함수  index, append, insert, pop, count, sort, reverse, clear, extend

mix_list = ["조세호", 20, True]
print(mix_list[0][1])

cabinet = {3: "유재석", 100:"김태호"}
print(cabinet[3])
print(cabinet.get(5)) # get을 이용하면 값이 없을 경우 None 값이 할당 됨
print(cabinet.get(5, "사용 가능")) # key가 5인 것을 찾고 없으면 "사용 가능" 이 할당 됨
print(3 in cabinet) # True , cabinet이라는 dictionary에 3 이라는 key가 있는 지 없는 지
# key와 value 추가
cabinet["C-20"] = "조세호" # 기존에 있던 key가 들어가면 value 값이 업데이트 됨
del cabinet["C-20"] # key와 value 삭제
print(cabinet)

name, age, hobby = "김종국", 20, "운동"
#age +=1
print(name, age, hobby)

#set 은 중복 안되고, 순서가 없음
my_set = {1,2,3,3,3}
print(my_set)

ids = list(range(1,21))
shuffle(ids)
chicken = sample(ids, 1)
ids.remove(chicken[0])
coffee = sorted(sample(ids, 3))

print(" -- 당첨자 발표 --")
print("치킨 당첨자 :", chicken)
print("커피 당첨자 : ", coffee)
print(" -- 축하합니다 --")

# 한 줄 for문
students = [i for i in range(1,6)]
print(students)
students = [i+100 for i in students]
print(students)

students = ["Iron man", "Thor", "I am groot"]
students = [len(i)-i.count(" ") for i in students]
print(students)

pass_num = 1
att_num = 0
while pass_num <= 50:
    req_time = randint(5,50)
    mark = " "
    if 5 <=req_time<=15:
        mark = "O"
        att_num +=1
    print("[{0}] {1}번째 손님 (소요시간 : {2}분)".format(mark, pass_num, req_time))
    if pass_num == 50:
        print("총 탑승 승객 : {} 분".format(att_num))
    pass_num +=1

