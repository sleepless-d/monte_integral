from random import *
from sympy import * 

x = symbols('x')

def integral(expr,monte_cnt,sran,eran): # count(int),시작 x값(float),끝 x값(float)  //범위 임의의 값~임의의 값, 수식 자유 입력
    var_x = 0 #랜덤하게 할당할 x값, y값
    var_y = 0
    cnt_t = 0 #참 or 거짓 point들
    cnt_f = 0
    integralsum = 0 #구간별 적분 넓이의 '누적'합
    secarea = 0 #구간별 적분 넓이
    secpm = [] #양수 구간, 음수 구간 판독 배열, True(양수) or False(음수)로 저장

    try: #구간에 0이 있는지 없는지 체크.
        zeroval = list(solveset(expr,x,Interval(sran,eran))) #함숫값 = 0 인 지점과 시작점, 끝점 체크
    except:
        zeroval = []
    if eran not in zeroval: #zeroval에 시작점과 끝점 추가, 정렬
        zeroval.append(eran)
    if sran not in zeroval:
        zeroval.append(sran)
    zeroval.sort()

    r = [[None]*monte_cnt for _ in range(len(zeroval)-1)] #구간별 대략적 함숫값 저장 배열 생성
    
    sran = float(N(sran)) #전체 구간의 길이를 float로 변환
    eran = float(N(eran))
    
    for i in range(len(zeroval)-1):     #대략적인 함숫값 확인
        print("\r",i+1,"번째 구간 00.00% 확인 완료", end="",sep="")
        intseclen = ((zeroval[i+1]-zeroval[i])/monte_cnt) #각 구간을 count개로 나눈 소구간의 길이
        for j in range(monte_cnt):    
            r[i][j] = N(expr.subs(x,zeroval[i]+intseclen*j))
            print("\r",i+1,"번째 구간 %.2f %% 확인 완료" % ((float(j+1)/monte_cnt) * 100), end="",sep="")
        secpm.append(N(expr.subs(x,(zeroval[i]+zeroval[i+1])/2))>0) # 양수 구간 / 음수 구간 판독 후 배열로 저장
        
    print("\n\n함수를 확인했습니다.\n계산을 시작합니다.")

    for i in range(len(zeroval)-1): #구간 갯수만큼 반복
        cnt_t = 0 #참인 점과 거짓인 점 갯수를 각 구간마다 초기화
        cnt_f = 0

        if secpm[i] == True: #그 구간 중앙값이 양수일 때(=양수 구간일 때)
            print("\r",i+1,"번째 구간 00.00% 계산 완료", end="",sep="")

            for j in range(monte_cnt): #각각의 구간마다 넓이 계산
                var_x = uniform(zeroval[i],zeroval[i+1])
                var_y = uniform(0,max(r[i]))

                if (N(expr.subs(x,var_x)) >= var_y): #그래프 안에 점이 들어 있으면 참인 것으로 판정
                    cnt_t += 1
                else:
                    cnt_f += 1

                print("\r",i+1,"번째 구간 %.2f%% 계산 완료" % ((float(j+1)/monte_cnt) * 100), end="",sep="")

            secarea = N((cnt_t/monte_cnt) * (zeroval[i+1]-zeroval[i]) * max(r[i])) #값 x 구간 가로 길이 x 구간 세로 길이
            integralsum += secarea #integralsum(적분 근삿값)에 더한다. 

        elif secpm[i] == False: #그 구간 중앙값이 음수일 때(=음수 구간일 때)
            print("\r",i+1,"번째 구간 00.00% 계산 완료", end="",sep="")

            for j in range(monte_cnt): #각각의 구간마다 넓이 계산
                var_x = uniform(zeroval[i],zeroval[i+1])
                var_y = uniform(0,-min(r[i])) #x축에 대칭시켜서 넓이 계산

                if (-N(expr.subs(x,var_x)) >= var_y): #그래프 안에 점이 안 들어 있으면 거짓인 것으로 판정
                    cnt_t += 1
                else:
                    cnt_f += 1
                
                print("\r",i+1,"번째 구간 %.2f%% 계산 완료" % ((float(j+1)/monte_cnt) * 100), end="",sep="")    

            secarea = N((cnt_t/monte_cnt) * (zeroval[i+1]-zeroval[i]) * -min(r[i])) # 값 x 구간 가로 길이 x 구간 세로 길이
            integralsum -= secarea #integralsum(적분 근삿값)에서 뺀다.
    print("\n")
    result = "적분 근삿값 = " + str(N(integralsum))
    return result

def main():
    expr = input("(수식(dx 미포함)) from (시작값) to (끝값) 형태로 입력하세요. ").split(" ")
    expr[0] = sympify(expr[0]) #수식
    expr[2] = sympify(expr[2]) #시작값
    expr[4] = sympify(expr[4]) #끝값
    monte_cnt = int(input("count를 입력하세요. "))
    print(integral(expr[0],monte_cnt,expr[2],expr[4]))


while True:
    try:
        main()
    except:
        print("다시 입력하세요.")
        pass
