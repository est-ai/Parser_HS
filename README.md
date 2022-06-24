# LL(1) Parser
- 목표: Context Free Grammar(CFG)에 해당하는 LL1 Parser의 문법을 만들어서 구현하기
  - [x] 연산자(+, -, *, /, (, )) 를 사용하는 사칙연산 CFG Rule 만들기
    - [x] 만들어진 CFG Rule 이 LL(1) parser로 parsing 할 수 있는 형태로 만들기
  - [x] 함수 기반의 parser 만들기
  - [x] output 은 Tree 형태로 만들기
  - [x] Tree를 Traverse 하면서 계산하는 evaluate 함수 만들기

## 1. 설계방안 
```python
# CFG Rule
Expr: Expr Increments
Increments: Increment Increments | ε
Increment: AddOp Expr

Expr: Factor Scalings
Scalings: Scaling Scalings | ε
Scaling: MulOp Factor
Factor: Number | Enclosed | Negative
Enclosed: ( Expr )
Negative: - Number

AddOp: + | -
MulOp: * | /

Number: 정규표현식으로 처리(int or float)
```