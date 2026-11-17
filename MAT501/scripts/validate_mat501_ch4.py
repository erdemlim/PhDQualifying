from pathlib import Path
import sys,json
import sympy as s
from pypdf import PdfReader
x,z=s.symbols('x z',positive=True)
N=18
records=[]
def L(y,co):return s.expand(co[0]*s.diff(y,x,2)+co[1]*s.diff(y,x)+co[2]*y)
def record(name,poly):
    terms=[str(v) for v in s.Add.make_args(s.expand(poly))]
    records.append({'name':name,'series':str(poly)});print('PASS',name)
def regular(name,sgn,which,a0,a1):
    a=[s.S(a0),s.S(a1)]+[s.S(0)]*(N-1)
    if which=='xy':
        for n in range(N-2):a[n+3]=-sgn*a[n]/((n+3)*(n+2))
        co=[1,0,sgn*x]
    elif which=='xyp':
        for n in range(N-1):a[n+2]=-sgn*n*a[n]/((n+2)*(n+1))
        co=[1,sgn*x,0]
    elif which=='xypy':
        for n in range(N-1):a[n+2]=-sgn*a[n]/(n+2)
        co=[1,sgn*x,sgn]
    y=sum(a[n]*x**n for n in range(N+1));res=L(y,co)
    for n in range(N-1):assert s.simplify(res.coeff(x,n))==0,(name,n,res)
    record(name,y)
    return a,y
regular('notes_xy',1,'xy',1,0)
regular('notes_xyp',1,'xyp',0,1)
regular('Q2_shifted_center',1,'xy',1,0)
regular('Q3',-1,'xyp',0,1)
regular('Q4',1,'xy',0,1)
regular('Q5',1,'xypy',1,0)
y=sum(x**n/s.Integer(n) for n in range(1,N+1))
res=L(y,[1-x,-1,0])
assert all(res.coeff(x,n)==0 for n in range(N-1))
assert s.limit((s.S(1)/(z+1))/(1/z),z,s.oo)==1
record('Q6_log_radius1',y)

def frob(name,r,F,step,k,co):
    a=[s.S(1)]+[s.S(0)]*N
    for n in range(1,N+1):
        den=s.factor(F(n+r));prev=a[n-step] if n>=step else s.S(0)
        assert den!=0,(name,n)
        a[n]=s.cancel(-k*prev/den)
    p=sum(a[n]*x**n for n in range(N+1));y=x**r*p
    res=s.expand(L(y,co)/x**r)
    for n in range(N+1):assert s.simplify(res.coeff(x,n))==0,(name,n,res)
    record(name,y)
    return p
for r in [s.S(0),s.Rational(1,2)]:
    frob('notes_noninteger_'+str(r),r,lambda v:v*(2*v-1),1,2,[2*x*x,x,2*x])
p=frob('notes_integer_log_large',s.S(2),lambda v:v*(v-2),1,1,[x*x,-x,x])
assert s.series(1/p**2,x,0,3).removeO()==1+s.Rational(2,3)*x+x*x/4
for r in [s.Rational(1,3),-s.Rational(1,3)]:
    frob('Q7_'+str(r),r,lambda v:v*v-s.Rational(1,9),2,1,[x*x,x,x*x-s.Rational(1,9)])
for r in [s.S(0),s.Rational(1,2)]:
    frob('Q8_'+str(r),r,lambda v:v*(2*v-1),1,-2,[2*x*x,x,-2*x])
frob('Q11_large',s.S(1),lambda v:v*v-1,2,1,[x*x,x,x*x-1])
p12=frob('Q12_large',s.S(1),lambda v:v*(v-1),1,1,[x*x,0,x])
assert s.series(1/p12**2,x,0,2).removeO()==1+x
assert L(s.exp(-x),[x,1+x,1])==0
assert L(s.exp(x),[x,1-x,-1])==0
assert L(s.S(1),[x*x,-x,0])==0
assert L(x*x,[x*x,-x,0])==0
assert L(s.S(1),[x*x,-2*x,0])==0
assert L(x**3,[x*x,-2*x,0])==0
# Reduced-order integrands responsible for logarithms.
assert s.simplify(s.exp(-s.integrate(1/x+1,x))/s.exp(-x)**2-s.exp(x)/x)==0
assert s.simplify(s.exp(-s.integrate(1/x-1,x))/s.exp(x)**2-s.exp(-x)/x)==0
print('PASS repeated roots and reduction of order')

out=Path(__file__).resolve().parents[1]/'tmp/pdfs'
out.mkdir(parents=True,exist_ok=True)
(out/'chapter4_preflight.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
for name,count in [('MAT501_Chapter4_Anlatim_ve_Cozumler.pdf',13),('MAT501_Chapter4_Karisik_Alistirmalar.pdf',7)]:
    path=out.parents[1]/'output/pdf'/name;r=PdfReader(path)
    assert len(r.pages)==count,(name,len(r.pages))
    for i,p in enumerate(r.pages):
        t=p.extract_text() or '';assert '\ufffd' not in t,(name,i)
    print('PDF',name,'pages',len(r.pages),'bytes',path.stat().st_size)
print('ALL CHECKS PASSED')
