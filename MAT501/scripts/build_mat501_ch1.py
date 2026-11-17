from pathlib import Path
import sys, io, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
TMP=ROOT/'tmp/pdfs'; TMP.mkdir(parents=True,exist_ok=True)
EQDIR=TMP/'equations'; EQDIR.mkdir(exist_ok=True)
FONTDIR=Path(matplotlib.get_data_path())/'fonts'/'ttf'
pdfmetrics.registerFont(TTFont('Body',str(FONTDIR/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('BodyBold',str(FONTDIR/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('BodyItalic',str(FONTDIR/'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
NAVY=HexColor('#18354A'); TEAL=HexColor('#087E8B'); INK=HexColor('#263746'); PALE=HexColor('#EAF4F5')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.7,leading=14.4,textColor=INK,spaceAfter=6),
 'small':ParagraphStyle('small',fontName='Body',fontSize=9.2,leading=12.3,textColor=INK,spaceAfter=5),
 'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=13,leading=17,textColor=TEAL,spaceBefore=10,spaceAfter=6),
 'title':ParagraphStyle('title',fontName='BodyBold',fontSize=23,leading=28,textColor=NAVY,spaceAfter=8),
 'subtitle':ParagraphStyle('subtitle',fontName='Body',fontSize=11.2,leading=15,textColor=TEAL,spaceAfter=12),
 'box':ParagraphStyle('box',fontName='Body',fontSize=10.3,leading=14,textColor=NAVY),
}
story=[]; manifest=[]; page_specs=[]
def p(s,small=False): story.append(Paragraph(s,styles['small' if small else 'body']))
def h(s): story.append(Paragraph(s,styles['h2']))
def eq(s,result=False):
    # MathText requires explicit braces even where TeX permits single-token arguments.
    def arg(t,i):
        while i<len(t) and t[i].isspace(): i+=1
        if t[i]=='{':
            start=i+1; depth=1; i+=1
            while depth:
                if t[i]=='{': depth+=1
                elif t[i]=='}': depth-=1
                i+=1
            return t[start:i-1],i
        if t[i]=='\\':
            j=i+1
            while j<len(t) and t[j].isalpha(): j+=1
            return t[i:j],j
        return t[i],i+1
    normalized='';i=0
    while i<len(s):
        if s.startswith('\\frac',i):
            a,i=arg(s,i+5);b,i=arg(s,i);normalized+='\\frac{'+a+'}{'+b+'}'
        elif s.startswith('\\sqrt',i):
            a,i=arg(s,i+5);normalized+='\\sqrt{'+a+'}'
        else: normalized+=s[i];i+=1
    s=normalized
    key=hashlib.sha1(s.encode()).hexdigest()
    path=EQDIR/(key+'.png')
    if not path.exists():
        math_to_image('$'+s+'$',path,prop=FontProperties(size=13.2),dpi=220,format='png',color='#18354A')
    with PILImage.open(path) as im: w,hg=im.size
    wpt=w*72/220; hpt=hg*72/220
    if wpt>465:
        hpt*=465/wpt;wpt=465
    im=Image(str(path),width=wpt,height=hpt)
    im.hAlign='LEFT'
    if result:
        t=Table([[im]],colWidths=[475]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),0.5,HexColor('#C3DFE2')),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
        story.extend([Spacer(1,3),t,Spacer(1,7)])
    else: story.extend([Spacer(1,2),im,Spacer(1,7)])
    manifest.append(s)
def box(s):
    t=Table([[Paragraph(s,styles['box'])]],colWidths=[475]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));story.extend([t,Spacer(1,7)])
def page(title,sub):
    if story: story.append(PageBreak())
    page_specs.append(title)
    story.append(Paragraph(title,styles['title']))
    story.append(Paragraph(sub,styles['subtitle']))

page('MAT501 | Chapter 1','Birinci mertebe ODE: yöntem özeti ve birlikte çözülen örnekler')
p('Doktora yeterlik yazılı hazırlığı • 24 Ekim 2026',small=True)
box('<b>Amaç:</b> Denklemi tanı, uygun yöntemi seç, başlangıç koşulunu uygula, çözümü ve geçerlilik aralığını kontrol et. Bu dosya ders notunun yerine geçen tam bir kitap değil; soru çözme odaklı tekrar föyüdür.')
h('Yöntemi seçerken bakılacak biçimler')
rows=[['Biçim / işaret','İlk hamle'],
 ['y′ = f(x)g(y)','Değişkenleri ayır; bölmeyle kaybolan çözümleri kontrol et.'],
 ['y′ + P(x)y = Q(x)','Lineer: integrasyon çarpanı.'],
 ['y′ = F(y/x)','Homojen tip: u = y/x, y = xu.'],
 ['y′ = F(Ax + By + C)','u = Ax + By + C dönüşümü.'],
 ['y′ + Py = Qyⁿ','Bernoulli: v = y^(1-n), n ≠ 0, 1.'],
 ['M dx + N dy = 0','Önce Mᵧ = Nₓ kontrolü; exact ise Φ = C.'],
 ['y′ = ay² + by + c; yₚ biliniyor','Riccati: y = yₚ + 1/v.']]
data=[[Paragraph(c,styles['small']) for c in row] for row in rows]
t=Table(data,colWidths=[190,285],hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),0.4,HexColor('#DAE4E9')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t)
h('Dosyanın düzeni')
p('2-3: lineer • 4-5: ayrılabilir ve homojen tip • 6-8: Bernoulli • 9-12: exact ve çarpan • 13-15: Riccati • 16: birleşik değişken dönüşümü • 17: varlık-teklik • 18: son kontrol listesi.')
p('<b>Kaynak ayrımı:</b> Konu kapsamı klasördeki MAT501 Chapter 1 notlarına dayanır. Örnekler, birlikte çalıştığımız soruların doğru ve tamamlanmış çözümleridir. Doğrudan nottan alınan varlık-teklik örneği 17. sayfada ayrıca belirtilmiştir. Bunlar geçmiş yeterlik sorusu olarak sunulmamıştır.',small=True)

page('01 | Lineer denklemler','İntegrasyon çarpanı: sol tarafı bir çarpımın türevine dönüştür')
eq(r"y'+P(x)y=Q(x),\qquad \mu(x)=e^{\int P(x)\,dx}")
eq(r"(\mu y)'=\mu Q,\qquad y=\frac{\int\mu Q\,dx+C}{\mu}")
h('Örnek 1: değişken katsayılı lineer denklem')
eq(r"y'+\frac{2}{x}y=x^2,\qquad y(1)=2,\quad x>0")
p('P = 2/x olduğundan çarpan x². Denklemin tamamını bu çarpanla çarp:')
eq(r"(x^2y)'=x^4\quad\Longrightarrow\quad x^2y=\frac{x^5}{5}+C")
eq(r"y=\frac{x^3}{5}+\frac{C}{x^2},\qquad 2=\frac15+C")
eq(r"y=\frac{x^3}{5}+\frac{9}{5x^2},\qquad I=(0,\infty)",True)
h('Örnek 2: sabit katsayılı lineer denklem')
eq(r"y'+3y=6,\qquad y(0)=1")
eq(r"\mu=e^{3x},\qquad (e^{3x}y)'=6e^{3x}")
eq(r"e^{3x}y=2e^{3x}+C\quad\Longrightarrow\quad y=2+Ce^{-3x}")
eq(r"C=-1,\qquad y=2-e^{-3x},\qquad I=\mathbb{R}",True)
box('<b>Fiziksel yorum:</b> y′ = 3(2-y). y &lt; 2 iken artış, y &gt; 2 iken azalış var. y = 2 kararlı dengedir. Başlangıç değeri 1 olan çözüm 2’ye aşağıdan yaklaşır.')

page('02 | Lineer çözümü tamamlamak','Zorlama, homojen çözüm ve özel çözüm')
h('Örnek 3: sağ taraf x’e bağlı')
eq(r"y'+2y=4x,\qquad y(0)=1")
eq(r"\mu=e^{2x},\qquad (e^{2x}y)'=4xe^{2x}")
p('Sağ taraf için kısmi integrasyon: u = 4x, dv = e²ˣ dx.')
eq(r"\int4xe^{2x}\,dx=2xe^{2x}-e^{2x}+C")
eq(r"y=2x-1+Ce^{-2x},\qquad 1=-1+C")
eq(r"y=2x-1+2e^{-2x},\qquad I=\mathbb{R}",True)
h('İki farklı “homojen” kavramı')
p('<b>Homojen lineer:</b> y′ + Py = 0. Buradaki homojenlik, lineer denklemde zorlama teriminin sıfır olmasıdır. Örnek: y′ + 3y = 0.')
p('<b>Homojen tip:</b> y′ = F(y/x). Buradaki işaret, y = xu dönüşümüdür. Bu denklem lineer olmak zorunda değildir. Örnek: y′ = 1 + (y/x)².')
h('Homojen + özel çözüm ayrımı')
eq(r"y=y_h+y_p\qquad\text{(lineer denklemler)}")
p('y′ + 3y = 6 örneğinde sağ tarafı sıfır yapınca homojen çözüm, asıl denklemi sağlayan tek bir fonksiyon bulununca özel çözüm elde edilir:')
eq(r"y_h=Ce^{-3x},\qquad y_p=2,\qquad y=Ce^{-3x}+2")
box('Bu ayrım birinci mertebeyle sınırlı değildir. Yüksek mertebe lineer denklemlerde de kullanılacak. “General solution” genel çözüm; “homogeneous solution” homojen çözümdür.')

page('03 | Ayrılabilir ve homojen tip','Bölme sırasında kaybolan çözümlere dikkat')
h('Ayrılabilir biçim')
eq(r"y'=f(x)g(y)\quad\Longrightarrow\quad\frac{dy}{g(y)}=f(x)\,dx")
p('g(y) = 0 kökleri sabit çözümler verebilir; bu çözümleri bölmeden önce veya sonra ayrıca kontrol et.')
h('Örnek 4: arctan integrali')
eq(r"y'=(y-1)^2+1,\qquad y(0)=0")
eq(r"\frac{dy}{1+(y-1)^2}=dx\quad\Longrightarrow\quad\arctan(y-1)=x+C")
eq(r"C=-\frac\pi4,\qquad y=1+\tan\left(x-\frac\pi4\right)",True)
eq(r"I=\left(-\frac\pi4,\frac{3\pi}4\right)")
h('Homojen tip dönüşümü')
eq(r"y'=F(y/x),\qquad u=\frac yx,\qquad y'=u+xu'")
eq(r"xu'=F(u)-u")
h('Örnek 5: hem lineer hem homojen tip')
eq(r"y'=1+\frac yx,\qquad y(1)=0,\quad x>0")
eq(r"u+xu'=1+u\quad\Longrightarrow\quad u'=\frac1x")
eq(r"u=\ln x+C,\quad C=0,\quad y=x\ln x,\quad I=(0,\infty)",True)

page('04 | Karışık alıştırma 1','Yöntem seçimi + başlangıç koşulu + çözüm aralığı')
eq(r"x^2y'=xy+y^2,\qquad y(1)=1,\quad x>0")
h('1. Biçimi tanı')
eq(r"y'=\frac yx+\left(\frac yx\right)^2")
p('Sağ taraf yalnızca y/x’e bağlı: homojen tip. Bu soru Bernoulli olarak da çözülebilir.')
h('2. Dönüştür ve değişkenleri ayır')
eq(r"u=y/x,\qquad u+xu'=u+u^2\quad\Longrightarrow\quad xu'=u^2")
eq(r"\frac{du}{u^2}=\frac{dx}{x}\quad\Longrightarrow\quad-\frac1u=\ln x+C")
h('3. Geri dön ve koşulu uygula')
eq(r"y=-\frac{x}{\ln x+C},\qquad 1=-\frac1C\quad\Longrightarrow\quad C=-1")
eq(r"y=\frac{x}{1-\ln x}",True)
h('4. Geçerlilik aralığı')
p('x pozitif olmalı. Payda x = e’de sıfır olur. Başlangıç noktası 1’i içeren en geniş açık aralık seçilir:')
eq(r"I=(0,e)",True)
box('<b>Kaybolan çözüm:</b> u²’ye böldüğümüz için u = 0, yani y = 0 çözümünü ayrıca kontrol ederiz. Denklemi sağlar ama y(1) = 1’i sağlamaz.')

page('05 | Bernoulli dönüşümü','Kuvveti değiştirerek lineer denkleme geç')
eq(r"y'+P(x)y=Q(x)y^n,\qquad n\ne0,1")
eq(r"v=y^{1-n},\qquad v'=(1-n)y^{-n}y'")
eq(r"v'+(1-n)Pv=(1-n)Q",True)
h('Örnek 6: n = 2')
eq(r"y'+y=xy^2,\qquad y(0)=1")
p('v = 1/y seç. Denklemi y²’ye böl:')
eq(r"\frac{y'}{y^2}+\frac1y=x\quad\Longrightarrow\quad-v'+v=x")
eq(r"v'-v=-x,\qquad \mu=e^{-x},\qquad(e^{-x}v)'=-xe^{-x}")
eq(r"e^{-x}v=(x+1)e^{-x}+C\quad\Longrightarrow\quad v=x+1+Ce^x")
p('Başlangıç koşulunu dönüştür: v(0) = 1. Buradan C = 0.')
eq(r"y=\frac1{x+1},\qquad I=(-1,\infty)",True)
box('<b>Kontrol:</b> y′ + y = -1/(x+1)² + 1/(x+1) = x/(x+1)² = xy². Bölme sırasında dışarıda kalan y = 0 da bir çözümdür; başlangıç koşulunu sağlamaz.')

page('06 | Bernoulli ve işaretler','Mutlak değer, kök seçimi ve negatif x bölgesi')
h('Örnek 7')
eq(r"y'+\frac1x y=xy^3,\qquad y(1)=1,\quad x>0")
eq(r"v=y^{-2},\quad v'=-2y^{-3}y',\quad-\frac{v'}2+\frac vx=x")
eq(r"v'-\frac2xv=-2x,\qquad\mu=x^{-2}")
eq(r"(x^{-2}v)'=-\frac2x\quad\Longrightarrow\quad x^{-2}v=-2\ln x+C")
eq(r"v=x^2(C-2\ln x),\qquad v(1)=1\quad\Longrightarrow\quad C=1")
eq(r"y=\frac1{x\sqrt{1-2\ln x}},\qquad I=(0,\sqrt e)",True)
h('x negatif verilirse ne değişir?')
p('İşlemde ln|x| kullanılır. Çarpan yine |x|⁻² = x⁻² olur. Ancak y(1) = 1 koşulu negatif x aralığında kullanılamaz; başlangıç noktası da o aralıkta olmalı.')
eq(r"\frac1{y^2}=x^2(C-2\ln|x|),\qquad y=\frac{\pm1}{|x|\sqrt{C-2\ln|x|}}")
p('Örneğin y(-1) = 1 olsaydı C = 1 ve pozitif dal seçilirdi:')
eq(r"y=\frac1{(-x)\sqrt{1-2\ln(-x)}},\qquad I=(-\sqrt e,0)")
box('Kökün işaretini x’in değil başlangıçtaki y’nin işareti belirler. Her zaman √(x²) = |x| ve ∫dx/x = ln|x| + C kullan.')

page('07 | Karışık alıştırma 3','Bernoulli: üstel zorlama ve sonlu x’te büyüme')
eq(r"y'+y=e^xy^3,\qquad y(0)=1")
h('1. Bernoulli dönüşümü')
eq(r"v=y^{-2},\qquad -\frac{v'}2+v=e^x\quad\Longrightarrow\quad v'-2v=-2e^x")
h('2. Lineer denklemi çöz')
eq(r"\mu=e^{-2x},\qquad(e^{-2x}v)'=-2e^{-x}")
eq(r"e^{-2x}v=2e^{-x}+C\quad\Longrightarrow\quad v=2e^x+Ce^{2x}")
h('3. Başlangıç koşulu ve geri dönüş')
eq(r"v(0)=1\quad\Longrightarrow\quad C=-1,\qquad v=2e^x-e^{2x}")
eq(r"y=\frac1{\sqrt{2e^x-e^{2x}}}",True)
h('4. Aralık ve kaybolan çözüm')
eq(r"2e^x-e^{2x}=e^x(2-e^x)>0\quad\Longrightarrow\quad x<\ln2")
eq(r"I=(-\infty,\ln2)",True)
p('y = 0 dönüşüm sırasında dışarıda kalan çözümdür; verilen başlangıç koşulunu sağlamaz. x, ln2’ye soldan yaklaşırken payda sıfıra yaklaşır ve y sınırsız büyür.')

page('08 | Exact denklemler','Bir potansiyel fonksiyonun toplam diferansiyelini bul')
eq(r"M\,dx+N\,dy=0,\qquad M_y=N_x\quad\Longrightarrow\quad d\Phi=0")
p('Sürekli kısmi türevlerle, uygun basit bağlantılı bölgede bu kontrol exactlığı verir. Örneklerimizde yerel olarak veya tüm düzlemde bu koşul sağlanır.')
eq(r"\Phi_x=M,\qquad\Phi_y=N,\qquad\Phi(x,y)=C")
h('Örnek 8: kübik terimli potansiyel')
eq(r"2xy\,dx+(x^2+2y)\,dy=0")
eq(r"M_y=N_x=2x,\qquad\Phi=\int2xy\,dx=x^2y+g(y)")
eq(r"\Phi_y=x^2+g'(y)=x^2+2y\quad\Longrightarrow\quad g(y)=y^2")
eq(r"x^2y+y^2=C",True)
h('Örnek 9: başlangıç koşullu exact denklem')
eq(r"(2x+y)\,dx+(x+2y)\,dy=0,\qquad y(0)=1")
eq(r"M_y=N_x=1,\qquad\Phi=x^2+xy+g(y)")
eq(r"\Phi_y=x+g'(y)=x+2y\quad\Longrightarrow\quad g(y)=y^2")
eq(r"x^2+xy+y^2=1",True)
box('<b>İntegrasyon “sabiti”:</b> x’e göre integre edince g(y), y’ye göre integre edince g(x) eklenir. g(y)’nin içine xy gibi x’e bağlı bir terim konulamaz.')

page('09 | Karışık alıştırma 2','Exact çözümden, y’yi yalnız bırakmadan türev hesapla')
eq(r"(2xy+e^x)\,dx+(x^2+2y)\,dy=0,\qquad y(0)=1")
h('1. Exactlık kontrolü')
eq(r"M_y=2x=N_x")
h('2. Bu kez N’yi y’ye göre integre et')
eq(r"\Phi=\int(x^2+2y)\,dy=x^2y+y^2+g(x)")
eq(r"\Phi_x=2xy+g'(x)=2xy+e^x\quad\Longrightarrow\quad g(x)=e^x")
eq(r"x^2y+y^2+e^x=K")
p('x = 0 ve y = 1 yazınca K = 2:')
eq(r"x^2y+y^2+e^x=2",True)
h('3. y′(0)’ı hesapla')
p('Implicit çözümün iki tarafını x’e göre türevle:')
eq(r"2xy+x^2y'+2yy'+e^x=0")
eq(r"x=0,\ y=1\quad\Longrightarrow\quad2y'(0)+1=0")
eq(r"y'(0)=-\frac12",True)
box('Kısa kontrol: Asıl denklemden y′ = -(2xy + eˣ)/(x² + 2y). (0,1) noktasında yine -1/2 çıkar. Bu noktada payda sıfır olmadığı için y, yerel olarak x’in düzgün bir fonksiyonudur.')

page('10 | Exact değilse çarpan','Tek değişkene bağlı integrasyon çarpanları')
eq(r"\frac{M_y-N_x}{N}=f(x)\quad\Longrightarrow\quad\mu(x)=e^{\int f(x)\,dx}")
eq(r"\frac{N_x-M_y}{M}=g(y)\quad\Longrightarrow\quad\mu(y)=e^{\int g(y)\,dy}")
p('Oranın yalnızca belirtilen değişkene bağlı olması gerekir. Paydaların ve çarpanın sıfır olmadığı bölgede çalış. Bu iki test sonuç vermezse başka bir yöntem gerekebilir.')
h('Örnek 10: x’e bağlı çarpan')
eq(r"2y\,dx+x\,dy=0,\quad x>0:\qquad\frac{M_y-N_x}{N}=\frac1x")
eq(r"\mu=x,\qquad2xy\,dx+x^2\,dy=d(x^2y)=0")
eq(r"x^2y=C",True)
h('Örnek 11: y’ye bağlı çarpan')
eq(r"y\,dx+2x\,dy=0,\quad y>0:\qquad\frac{N_x-M_y}{M}=\frac1y")
eq(r"\mu=y,\qquad y^2\,dx+2xy\,dy=d(xy^2)=0")
eq(r"xy^2=C",True)
p('Aynı denklem x ≠ 0 için lineer olarak da çözülür: y′ + y/(2x) = 0. Çarpan √|x|, çözüm y = K/√|x|. y &gt; 0 koşulunda K &gt; 0; pozitif ve negatif x aralıkları ayrıdır.')
h('Başlangıçta sağ taraf sıfır değilse')
p('Önce bütün terimleri sola topla. Örneğin (2x+y)y′ + y = 3, (y-3)dx + (2x+y)dy = 0 olur. M ve N bu yeni biçimden okunur. Bu düzenleme “homojen lineer denklem” demek değildir.')

page('11 | Karışık alıştırma 4','Exactlığı çarpanla sağla, sonra potansiyeli kur')
eq(r"(y+1)\,dx+(2x+y^2)\,dy=0,\qquad y(0)=1,\quad y>-1")
h('1. Exact değil; uygun oranı kontrol et')
eq(r"M_y=1,\quad N_x=2,\qquad\frac{N_x-M_y}{M}=\frac1{y+1}")
eq(r"\mu(y)=e^{\int\frac{dy}{y+1}}=y+1")
h('2. Denklemin tamamını çarp')
eq(r"(y+1)^2\,dx+(y+1)(2x+y^2)\,dy=0")
p('Yeni çapraz türevlerin ikisi de 2(y+1). Artık exact.')
h('3. Potansiyel fonksiyonu bul')
eq(r"\Phi=x(y+1)^2+g(y)")
eq(r"\Phi_y=2x(y+1)+g'(y)=(y+1)(2x+y^2)")
eq(r"g'(y)=y^3+y^2\quad\Longrightarrow\quad g(y)=\frac{y^4}{4}+\frac{y^3}{3}")
h('4. Başlangıç koşulu')
eq(r"\Phi(0,1)=\frac14+\frac13=\frac7{12}")
eq(r"x(y+1)^2+\frac{y^4}{4}+\frac{y^3}{3}=\frac7{12}",True)
box('Alternatif yol: x’i y’nin fonksiyonu kabul edersen dx/dy + 2x/(y+1) = -y²/(y+1), lineer bir denklem elde edilir. İstenen özel bir yöntem yoksa geçerli kısa yolu seçebilirsin.')

page('12 | Riccati dönüşümü','Bilinen özel çözüm, lineerleştirmenin anahtarı')
eq(r"y'=a(x)y^2+b(x)y+c(x),\qquad y=y_p+\frac1v")
p('Önce verilen yₚ’yi yerine koyarak doğrula. yₚ gerçekten çözümse karesel v terimleri sadeleşir:')
eq(r"v'+(2ay_p+b)v=-a",True)
p('Dönüşüm yₚ çözümünü temsil etmez; o çözüm ayrıca tutulur. v = 0 noktalarında geri dönüş tanımsızdır.')
h('Örnek 12')
eq(r"y'=y^2-\frac2{x^2},\qquad y(1)=0,\quad x>0,\quad y_p=\frac1x")
p('Kontrol: yₚ′ = -1/x² = yₚ² - 2/x². Dönüşüm y = 1/x + 1/v.')
eq(r"-\frac1{x^2}-\frac{v'}{v^2}=-\frac1{x^2}+\frac2{xv}+\frac1{v^2}")
eq(r"v'+\frac2xv=-1,\qquad\mu=x^2,\qquad(x^2v)'=-x^2")
eq(r"v=-\frac x3+\frac C{x^2}")
p('y(1) = 0 koşulu v(1) = -1 verir; dolayısıyla C = -2/3.')
eq(r"v=-\frac{x^3+2}{3x^2},\qquad y=\frac1x-\frac{3x^2}{x^3+2}")
eq(r"y=\frac{2(1-x^3)}{x(x^3+2)},\qquad I=(0,\infty)",True)

page('13 | Riccati: katsayıların iptali','Yerine koy, grupla, sabit terimi kaybetme')
eq(r"y'=y^2+\left(\frac1x-2x\right)y+x^2,\qquad y(1)=0,\quad x>0")
p('Verilen yₚ = x için sağ taraf x² + 1 - 2x² + x² = 1 = yₚ′. Özel çözüm doğru.')
eq(r"y=x+\frac1v,\qquad y'=1-\frac{v'}{v^2}")
h('1. Açılımı sadeleştir')
eq(r"1-\frac{v'}{v^2}=x^2+\frac{2x}{v}+\frac1{v^2}+1-2x^2+\frac1{xv}-\frac{2x}{v}+x^2")
eq(r"1-\frac{v'}{v^2}=1+\frac1{v^2}+\frac1{xv}")
eq(r"-v'=1+\frac vx\quad\Longrightarrow\quad v'+\frac1xv=-1")
h('2. Lineer denklemi çöz')
eq(r"\mu=x,\qquad(xv)'=-x,\qquad v=-\frac x2+\frac Cx")
p('y(1) = 0 ⇒ v(1) = -1 ⇒ C = -1/2.')
eq(r"v=-\frac{x^2+1}{2x}")
h('3. y’ye geri dön')
eq(r"y=x+\frac1v=x-\frac{2x}{x^2+1}=\frac{x(x^2-1)}{x^2+1}",True)
p('Aralık: (0, ∞). Payda pozitif; denklem x = 0’da tanımsız. Bu özel çözüm fonksiyonunun 0’a uzatılabilmesi, verilen ODE’nin orada tanımlı olduğu anlamına gelmez.')
box('<b>İki işlem kontrolü:</b> v² ile çarpınca 1/v² terimi 1 olur; kaybolmaz. Son adımda y = yₚ + v değil, y = yₚ + 1/v yazılır.')

page('14 | Karışık alıştırma 5','Riccati’den ayrılabilir lineer denkleme')
eq(r"y'=y^2+(2-2x)y+x^2-2x+1,\qquad y(0)=1")
h('1. Özel çözümü doğrula')
eq(r"y_p=x:\qquad x^2+(2-2x)x+x^2-2x+1=1=y_p'")
h('2. Dönüşümü uygula')
eq(r"y=x+\frac1v\quad\Longrightarrow\quad1-\frac{v'}{v^2}=1+\frac2v+\frac1{v^2}")
eq(r"-v'=2v+1\quad\Longrightarrow\quad v'+2v=-1")
h('3. Kaldığımız integral')
eq(r"-\int\frac{dv}{2v+1}=\int dx\quad\Longrightarrow\quad-\frac12\ln|2v+1|=x+C")
eq(r"2v+1=Ae^{-2x},\qquad v=\frac{Ae^{-2x}-1}{2}")
p('y(0) = 1 ⇒ v(0) = 1 ⇒ A = 3. Ayırma sırasında dışarıda kalan v = -1/2 sabit çözümü bu koşulu sağlamaz.')
h('4. Geri dönüş ve aralık')
eq(r"y=x+\frac2{3e^{-2x}-1}",True)
eq(r"3e^{-2x}-1=0\quad\Longrightarrow\quad x=\frac{\ln3}{2}")
eq(r"I=\left(-\infty,\frac{\ln3}{2}\right)",True)
box('İntegralde 1/2 katsayısı paydanın türevi 2 olduğu için gelir. Alternatif: (e²ˣv)′ = -e²ˣ ile aynı sonuca ulaşılır.')

page('15 | Birleşik değişken dönüşümü','y′ = F(Ax + By + C) biçimi')
eq(r"u=Ax+By+C\quad\Longrightarrow\quad u'=A+By'=A+BF(u)")
p('B ≠ 0 ise yeni denklem ayrılabilir. Son adımda y = (u-Ax-C)/B ile dönülür. Sabit u çözümleri bölme sırasında kaybolabilir. B = 0 ise sağ taraf yalnızca x’e bağlıdır; doğrudan integral alınır.')
h('Örnek 13')
eq(r"y'=(x+y)^2,\qquad y(0)=0")
h('1. Birleşimi yeni değişken yap')
eq(r"u=x+y,\qquad u'=1+y'=1+u^2,\qquad u(0)=0")
h('2. Değişkenleri ayır ve integre et')
eq(r"\frac{du}{1+u^2}=dx\quad\Longrightarrow\quad\arctan u=x+C")
eq(r"u(0)=0\quad\Longrightarrow\quad C=0,\qquad u=\tan x")
h('3. Asıl değişkene dön')
eq(r"y=\tan x-x,\qquad I=\left(-\frac\pi2,\frac\pi2\right)",True)
h('4. Yerine koyarak kontrol')
eq(r"y'=\sec^2x-1=\tan^2x=(x+y)^2")
box('Burada türev alırken u′ = y′ yazılmaz: u = x+y olduğu için u′ = 1+y′. Dönüşümün asıl faydası, birbirine karışmış x ve y’yi tek bir u değişkeninde toplamasıdır.')

page('16 | Varlık, teklik ve aralık','Çözümün var olması, tek olması ve her yerde sürmesi farklı iddialardır')
h('Yerel varlık-teklik kontrolü')
eq(r"y'=f(x,y),\qquad y(x_0)=y_0")
p('<b>Varlık:</b> f, başlangıç noktasını içeren açık bir dikdörtgende sürekli ise yerel en az bir çözüm vardır. <b>Teklik:</b> Ayrıca fᵧ sürekli ise bu çözüm yerel olarak tektir. Bu, yeterli bir kriterdir; kriterin sağlanmaması tek başına çoklu çözüm kanıtı değildir.')
h('Örnek 14: doğrudan ders notundan (Chapter 1, s. 5)')
eq(r"y'=x^2+\frac xy,\qquad y(1)=3,\qquad f_y=-\frac{x}{y^2}")
p('f ve fᵧ, R = (0,2) × (2,4) dikdörtgeninde sürekli. (1,3) bu bölgenin içinde. Dolayısıyla 1’in yeterince küçük bir çevresinde çözüm vardır ve tektir. Burada y(x)’i bulmamız gerekmez.')
h('Örnek 15: çözüm var, ama tek değil')
eq(r"y'=\sqrt{|y|},\qquad y(0)=0")
p('f sürekli: varlık var. y = 0’da fᵧ yok: standart teklik garantisi uygulanamaz. Tekliğin bozulduğunu iki farklı çözümle gösteririz:')
eq(r"y_1(x)=0;\qquad y_2(x)=0\ (x\leq0),\quad y_2(x)=x^2/4\ (x>0)")
p('y₂’nin türevi 0’ın her iki yanında 0’a yaklaşır ve y₂′(0) = 0. x &gt; 0 için y₂′ = x/2 = √(x²/4); x ≤ 0 için iki taraf sıfır. İkisi de başlangıç koşulunu sağlar; çözüm tek değildir.')
p('x²/4 nereden geldi? y &gt; 0 bölgesinde dy/√y = dx ⇒ 2√y = x+C. 0’a ulaşan dal için C = 0; x ≥ 0’da y = x²/4. y = 0, bölme sırasında dışarıda kalan sabit çözümdür.',small=True)
h('En geniş çözüm aralığı nasıl seçilir?')
p('Başlangıç noktasını içeren, hem ODE’nin hem çözümün tanımlı kaldığı en geniş açık aralığı al. Paydanın sıfırlarını, logaritmayı, karekökün içini ve tanjant kutuplarını kontrol et. Yerel teklik, çözümün tüm gerçek eksende devam etmesini garanti etmez.')

page('17 | Sınav öncesi son tekrar','Yöntem bilgisi + işlem disiplini')
h('Bir soruyu bitirmeden önce')
for s in [
 '1. Standart biçimi yaz: y′ yalnız mı; M dx + N dy = 0 biçimi doğru mu?',
 '2. Yöntemini belirt: hangi özellik hangi dönüşümü öneriyor?',
 '3. Yeni değişkenin türevini açıkça yaz; katsayı ve işaretleri bu satırda kontrol et.',
 '4. Başlangıç koşulunu yeni değişkene taşı veya geri dönüşten sonra uygula.',
 '5. Bölme sırasında dışarıda kalan sabit/özel çözümleri kontrol et.',
 '6. Bulduğun çözümü asıl denkleme ve başlangıç koşuluna geri koy.',
 '7. En geniş çözüm aralığını, başlangıç noktasını içerecek şekilde belirt.']:
 p(s)
h('Bu çalışmada en çok dikkat isteyen adımlar')
p('İntegrasyon çarpanına bölerken C de bölünür. ∫y dx = xy; y, x’e göre sabittir. Exact çözümde g(y) yalnızca y’ye bağlıdır. Riccati’de dönüşüm sonunda 1/v alınır. Karekök ve logaritmada mutlak değer ve dal seçimi korunur.')
h('Küçük integral kartı')
eq(r"\int x^m\,dx=\frac{x^{m+1}}{m+1}+C\ (m\ne-1),\qquad\int\frac{dx}{x}=\ln|x|+C")
eq(r"\int\frac{dv}{av+b}=\frac1a\ln|av+b|+C\ (a\ne0)")
eq(r"\int\frac{du}{1+u^2}=\arctan u+C,\qquad\int e^{ax}\,dx=\frac1a e^{ax}+C\ (a\ne0)")
h('Kaynak ve kapsam')
p('Ana kaynak: MATH501_AdvancedEngineeringMathematics / Math501_Chapter1.pdf, 20 sayfa. Varlık-teklik örneği notun 5. sayfasından; diğer örnekler bu sohbetteki hazırlık sorularından derlenmiştir. Exact olmayan denklemlerde tek değişkenli integrasyon çarpanı, sorular üzerine eklenen tamamlayıcı yöntemdir.',small=True)
p('Sohbette hatalı kurulup sonradan düzeltilen soru biçimleri burada tekrar edilmemiştir. Çalışılan y′ = F(Ax+By+C), lineer, Bernoulli, homojen tip, exact ve Riccati kapsamı korunmuştur. Sonraki adım: Chapter 2, yüksek mertebe lineer ODE.',small=True)

def footer(c,doc):
    w,hg=A4
    c.setStrokeColor(TEAL);c.setLineWidth(1.2);c.line(53,hg-36,w-53,hg-36)
    c.setFont('Body',8.4);c.setFillColor(INK)
    c.drawString(53,hg-27,'MAT501 • Chapter 1 • Soru odaklı tekrar')
    c.setStrokeColor(HexColor('#DAE4E9'));c.setLineWidth(.4);c.line(53,43,w-53,43)
    c.drawString(53,29,'Yeterlik hazırlığı | 24.10.2026')
    c.drawRightString(w-53,29,f'{doc.page} / 18')

dest=OUT/'MAT501_Chapter1_Ozet_ve_Cozumler.pdf'
doc=SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=60,leftMargin=60,topMargin=57,bottomMargin=57,title='MAT501 Chapter 1 - Özet ve Çözümler',author='MAT501 Yeterlik Hazırlığı',pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(TMP/'equations_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(TMP/'page_titles.json').write_text(json.dumps(page_specs,ensure_ascii=False,indent=2),encoding='utf8')
print(dest)
print('Intended pages:',len(page_specs),'Equations:',len(manifest))
