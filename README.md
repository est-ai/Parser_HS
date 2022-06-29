# LL(1) Parser
- 목표: Context Free Grammar(CFG)에 해당하는 LL1 Parser의 문법을 만들어서 구현하기
  - [x] 연산자(+, -, *, /, (, )) 를 사용하는 사칙연산 CFG Rule 만들기
    - [x] 만들어진 CFG Rule 이 LL(1) parser로 parsing 할 수 있는 형태로 만들기
  - [x] 함수 기반의 parser 만들기
  - [x] output 은 Tree 형태로 만들기
  - [x] Tree를 Traverse 하면서 계산하는 evaluate 함수 만들기
- 1차피드백
  - [x] token의 return 방식 변경
  - [x] Parser 에서 advance, expect 정리
  - [x] Number의 is_valid 함수 수정
  - [x] evaluate 함수에서 1 depth를 넘게 보지 않도록 하기
  - [x] tree를 operation 별로 분리하는 것을 추천

  - [x] 괄호 앞 음수 처리 완료

## 1. 설계방안 
```python
# CFG Rule
Expr: Term Increments
Increments: Increment Increments | ε
Increment: AddOp Term

Term: Factor Scalings
Scalings: Scaling Scalings | ε
Scaling: MulOp Factor
Factor: Number | Enclosed | - Negative
Enclosed: ( Expr )
Negative: Number | Enclosed

AddOp: + | -
MulOp: * | /

Number: 정규표현식으로 처리(int or float)
```

## 2. Input Spec
- 사용가능한 연산자는 +, -, *, /, (, ) 총 6가지로 정의한다.
- 사용가능한 피연산자는 정수(int), 소수점(float), 음수(negative number) 를 모두 포함한다.
- 소수점은 소수점 앞과 뒤의 정수를 넣어 표현하는 것으로 제한한다.
  - 예를들어 .2, 2. 이런 표현식은 제한함
- 연산자와 피연산자 사이의 공백을 허용한다. 
- 괄호 앞 - 부호가 붙은 경우 허용
