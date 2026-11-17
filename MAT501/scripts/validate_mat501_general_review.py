from pathlib import Path
import json
import sympy as s
x,t,lam,alpha,C1,C2=s.symbols('x t lambda alpha C1 C2',real=True)
xp=s.symbols('xp',positive=True)
def L(y,co):return s.simplify(sum(c*s.diff(y,x,len(co)-1-i) for i,c in enumerate(co)))
checks=[]
def ok(name,condition):
    assert condition,name
    checks.append(name);print('PASS',name)

y=x*s.exp(C1*x)
ok('Q1 positive general solution (x>0)',s.simplify(s.diff(y,x)-y/x*(1+C1*x))==0)
ok('Q1 IVP',s.simplify(y.subs({x:1,C1:1})-s.E)==0)
y=(s.exp(lam*x)-s.exp(x)*(1+(lam-1)*x))/(lam-1)**2
ok('Q2 nonresonant ODE',s.simplify(L(y,[1,-2,1])-s.exp(lam*x))==0)
ok('Q2 initial conditions',s.simplify(y.subs(x,0))==0 and s.simplify(s.diff(y,x).subs(x,0))==0)
ok('Q2 resonant limit',s.simplify(s.limit(y,lam,1)-x*x*s.exp(x)/2)==0)
ok('Q3 analytic particular solution',L(x,[1-x*x,-2*x,2])==0)
y=s.sqrt(1-x*x)
ok('Q4 circle IVP',s.simplify(x+y*s.diff(y,x))==0 and y.subs(x,0)==1)
y=s.exp(x)+s.exp(-x)-2-x*x
ok('Q5 ODE and IC',s.simplify(L(y,[1,0,-1,0])-2*x)==0 and all(s.diff(y,x,k).subs(x,0)==0 for k in range(3)))
ok('Q5 first nonzero Taylor term',s.series(y,x,0,6).removeO()==x**4/12)
a=[s.S(0),s.S(1)]+[s.S(0)]*8
for n in range(8):a[n+2]=-a[n]/(n+2)
p=sum(a[n]*x**n for n in range(10))
ok('Q6 recurrence and four terms',[a[n] for n in [1,3,5,7]]==[s.S(1),-s.Rational(1,3),s.Rational(1,15),-s.Rational(1,105)])
ok('Q6 series residual',all(s.expand(L(p,[1,x,1])).coeff(x,n)==0 for n in range(8)))
ok('Q7 omitted special solution',s.simplify(s.diff(x,x)-(x*x-2*x*x+x*x+1))==0)
y=xp*xp*(C1+C2*s.log(xp))
ok('Q8 both endpoint limits',s.limit(y,xp,0,dir='+')==0 and s.limit(s.diff(y,xp),xp,0,dir='+')==0)
for r,coeff in [(s.Rational(1,2),[1,-s.Rational(1,6),s.Rational(1,120)]),(-s.Rational(1,2),[1,-s.Rational(1,2),s.Rational(1,24)])]:
    b=[s.S(1),s.S(0)]+[s.S(0)]*7
    for n in range(2,9):b[n]=-b[n-2]/((n+r)**2-s.Rational(1,4))
    ok('Q9 branch '+str(r),[b[0],b[2],b[4]]==coeff)
ok('Q9 exact large branch',s.simplify(L(s.sin(x)/s.sqrt(x),[x*x,x,x*x-s.Rational(1,4)]))==0)
ok('Q9 exact small branch',s.simplify(L(s.cos(x)/s.sqrt(x),[x*x,x,x*x-s.Rational(1,4)]))==0)
y=x*(1+x)*s.log((1+x)/x)
ok('Q10 particular solution',s.simplify(L(y,[x*x,-2*x,2])-x/(1+x))==0)
y=x*s.sin(2*x)/4+(s.cos(2*x)-s.cos(3*x))/5
ok('Q11 ODE',s.simplify(L(y,[1,0,4])-s.cos(2*x)-s.cos(3*x))==0)
ok('Q11 IC',y.subs(x,0)==0 and s.diff(y,x).subs(x,0)==0)
# Smaller-root equations: -a1+alpha*a0=0 and alpha*a1-a0=0.
ok('Q12 compatibility',s.solve(alpha**2-1,alpha)==[-1,1])
for v in [-1,1]:
    ok('Q12 analytic solution '+str(v),s.simplify(L(s.exp(v*x),[x*x,-x,v*x-x*x]))==0)
    ok('Q12 second analytic solution '+str(v),s.simplify(L((1+2*v*x)*s.exp(-v*x),[x*x,-x,v*x-x*x]))==0)
(Path(__file__).resolve().parents[1]/'tmp/pdfs').mkdir(parents=True,exist_ok=True)
(Path(__file__).resolve().parents[1]/'tmp/pdfs/general_review_validation.json').write_text(json.dumps({'checks':checks,'count':len(checks)},ensure_ascii=False,indent=2),encoding='utf8')
print('ALL',len(checks),'CHECKS PASSED')
