import sys,json
from pathlib import Path
import sympy as s
from pypdf import PdfReader
x=s.symbols('x',positive=True)
C1,C2,C3,C4=s.symbols('C1 C2 C3 C4')
def L(y,co):return sum(c*s.diff(y,x,len(co)-1-i) for i,c in enumerate(co))
def check(label,y,co,rhs=0,ic=None):
    residual=s.simplify(s.trigsimp(L(y,co)-rhs))
    assert residual==0,(label,residual)
    if ic:
        point,values=ic
        for order,value in enumerate(values):
            assert s.simplify(s.diff(y,x,order).subs(x,point)-value)==0,(label,order)
    print('PASS',label)
    return {'label':label,'solution':str(y)}

records=[]
records.append(check('notes1',2*s.exp(x)-s.exp(2*x),[1,-3,2],ic=(0,[1,0])))
records.append(check('notes2',2*s.exp(-2*x)-s.exp(-3*x),[1,5,6],ic=(0,[1,-1])))
records.append(check('notes3',(1+2*x)*s.exp(-2*x),[1,4,4],ic=(0,[1,0])))
records.append(check('notes4',(2-5*x)*s.exp(3*x),[1,-6,9],ic=(0,[2,1])))
records.append(check('notes5',s.exp(-x)*(s.cos(2*x)+s.sin(2*x)/2),[1,2,5],ic=(0,[1,0])))
records.append(check('notes6',s.exp(x)*(2*s.cos(3*x)-s.sin(3*x)),[1,-2,10],ic=(0,[2,-1])))
records.append(check('notes9',2*x+4,[1,-3,2],4*x+2))
records.append(check('notes10',-2*s.exp(-2*x)+5*s.exp(-x)+2*x-3,[1,3,2],4*x,ic=(0,[0,1])))
records.append(check('notes11',s.exp(3*x)/2,[1,-3,2],s.exp(3*x)))
records.append(check('notes12',-x*s.exp(x),[1,-3,2],s.exp(x)))
records.append(check('notes13',3*(x-1)*s.exp(-x)+3*s.exp(-2*x),[1,3,2],3*s.exp(-x),ic=(0,[0,0])))
records.append(check('notes14',(s.cos(x)+s.sin(x))/2,[1,1,2],s.cos(x)))
records.append(check('notes15',x*s.sin(x)/2,[1,0,1],s.cos(x)))
records.append(check('notes16',x*x*s.exp(x)/2,[1,-2,1],s.exp(x)))
records.append(check('notes17',s.exp(2*x)*(x/s.Integer(3)-s.Rational(1,9)),[1,0,-1],s.exp(2*x)*(x+1)))
records.append(check('notes18',(C1+C2*x)*s.exp(x)+C3*s.exp(-x),[1,-1,-1,1]))
records.append(check('notes19',(C1+C2*x+C3*x*x)*s.exp(x),[1,-3,3,-1]))
records.append(check('notes_variation',s.cos(x)*s.log(s.cos(x))+x*s.sin(x),[1,0,1],1/s.cos(x)))
records.append(check('notes20',(x**3+1/x)/2,[x*x,-x,-3],ic=(1,[1,1])))
records.append(check('notes21',x*x*(C1+C2*s.log(x)),[x*x,-3*x,4]))
records.append(check('notes22',C1*s.cos(2*s.log(x))+C2*s.sin(2*s.log(x)),[x*x,x,4]))
records.append(check('notes_Euler_force',x*x*(C1+C2*s.log(x)+s.log(x)**2/2),[x*x,-3*x,4],x*x))

# Private preflight solutions; these are not embedded in the exercise PDF.
records.append(check('Q1',s.Rational(2,5)*s.exp(3*x)+s.Rational(3,5)*s.exp(-2*x),[1,-1,-6],ic=(0,[1,0])))
records.append(check('Q2',(2+5*x)*s.exp(-3*x),[1,6,9],ic=(0,[2,-1])))
records.append(check('Q3',s.exp(-2*x)*(s.cos(3*x)+s.sin(3*x)),[1,4,13],ic=(0,[1,1])))
records.append(check('Q4',C1*s.exp(2*x)+C2*s.exp(-x),[1,-1,-2]))
records.append(check('Q5',-2*s.exp(-x)+s.exp(-2*x)/2+x*x-x+s.Rational(3,2),[1,3,2],2*x*x+4*x+2,ic=(0,[0,0])))
records.append(check('Q6',4*s.exp(2*x)-4*(1+x)*s.exp(x),[1,-3,2],4*s.exp(x),ic=(0,[0,0])))
records.append(check('Q7',s.exp(2*x)*(1-2*x+3*x*x),[1,-4,4],6*s.exp(2*x),ic=(0,[1,0])))
records.append(check('Q8',s.exp(-x)*(C1*s.cos(2*x)+C2*s.sin(2*x))-s.cos(x)+2*s.sin(x),[1,2,5],10*s.sin(x)))
records.append(check('Q9',C1*s.cos(x)+C2*s.sin(x)+2*x+x*s.sin(x)/2,[1,0,1],2*x+s.cos(x)))
records.append(check('Q10',(C1+C2*x)*s.exp(x)+(C3+C4*x)*s.exp(-x),[1,0,-2,0,1]))
records.append(check('Q11',C1*s.cos(x)+C2*s.sin(x)-x*s.cos(x)+s.sin(x)*s.log(s.sin(x)),[1,0,1],1/s.sin(x)))
records.append(check('Q12',C1+C2*s.exp(x)+x*s.exp(x)-(1+s.exp(x))*s.log(1+s.exp(x)),[2,-2,0],2*s.exp(x)/(1+s.exp(x))))
records.append(check('Q13',x*x+x**-2,[x*x,x,-4],ic=(1,[2,0])))
records.append(check('Q14',x*x*(s.log(x)+s.log(x)**2),[x*x,-3*x,4],2*x*x,ic=(1,[0,1])))

for a,b,target in [(s.exp(-2*x),s.exp(-3*x),-s.exp(-5*x)),(s.exp(3*x),x*s.exp(3*x),s.exp(6*x)),(s.exp(2*x),s.exp(-x),-3*s.exp(x))]:
    assert s.simplify(a*s.diff(b,x)-s.diff(a,x)*b-target)==0

out=Path(__file__).resolve().parents[1]/'tmp/pdfs'
out.mkdir(parents=True,exist_ok=True)
(out/'chapter2_preflight.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
for name,expected in [('MAT501_Chapter2_Anlatim_ve_Cozumler.pdf',16),('MAT501_Chapter2_Karisik_Alistirmalar.pdf',8)]:
    p=out.parents[1]/'output/pdf'/name
    r=PdfReader(p)
    assert len(r.pages)==expected,(name,len(r.pages))
    print(name,'PAGES',len(r.pages),'BYTES',p.stat().st_size)
    for i,page in enumerate(r.pages):
        t=page.extract_text() or ''
        assert '\ufffd' not in t,(name,i)
        print(i+1,t.split('\n')[4:6])
print('ALL CHECKS PASSED')
