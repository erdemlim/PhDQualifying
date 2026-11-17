from pathlib import Path
import json,sys

base=Path(__file__).with_name('build_mat501_ch1.py').read_text(encoding='utf8')
exec(base.split("page('MAT501 | Chapter 1'")[0])
part=Path(__file__).with_name('build_mat501_ch2.py').read_text(encoding='utf8')
helpers=part[part.index('def table('):part.index("page('MAT501 | Chapter 2'")]
exec(helpers.replace('Chapter 2','Genel tekrar').replace('24.10.2026','17.11.2026'))
qpart=part[part.index('def question('):part.index("page('MAT501 | Chapter 2','Karışık")]
exec(qpart)

page('MAT501 | Genel tekrar 01','Chapter 1, 2 ve 4 • 12 yeni karışık soru • 17 Kasım 2026')
box('<b>Kapsam:</b> Birinci mertebe ODE, yüksek mertebe lineer ODE, seri ve Frobenius. Yöntem başlıkları soru bazında verilmedi. Her soru için istenen sonucu gerekçelendir; farklı ama eşdeğer çözümler kabul edilir.')
p('Bu set kısa hesapların yanında yöntem seçimi, çözüm aralığı, teklik, çakışma ve tekil noktaların etkisini değerlendirir. Tüm değişkenler ve parametreler soyuttur; fiziksel birim atanmamıştır.')
h('Çalışma düzeni')
p('Soruları önce yardım almadan çöz. Sonuçlarını verilen denkleme ve varsa başlangıç koşullarına geri koy. Kapalı biçim elde etmek zorunlu değilse seri veya açıkça tanımlanmış integral biçimi kabul edilir. İşlem sırasında bir ifadeye bölüyorsan dışarıda kalan durumları da değerlendir.')
h('Kaynak ve düzey sınırı')
p('Klasörde MAT501’e ait gerçek vize örneği bulunamadığı için bu setin “vizeden bir kademe zor” olduğu doğrulanmış değildir. Set, yüklenen Chapter 1, 2 ve 4 ders notlarının kapsamı ve birlikte çalışılan örnekler esas alınarak hazırlanmıştır. Final veya yeterlik düzeyi hakkında bir iddia içermez.')
p('Yeni alıştırmalarda, eldeki gerçek sınav örnekleriyle düzeyi karşılaştırma tercihi korunur. MAT501 vizesi eklendiğinde set bu referansa göre yeniden ayarlanabilir.',small=True)
h('Dosya içeriği')
p('12 soru, sayfa başına iki soru ve kısa çalışma alanı. Bu dosya cevap anahtarı içermez. Sorular sunulmadan önce çözüm, başlangıç koşulları ve istisna durumları kontrol edilmiştir.')

page('Sorular | 1-2','Yöntemini kendin seç ve sonucu kontrol et')
question(1,r"y'=\frac yx\left(1+\ln\frac yx\right),\qquad x>0,\quad y>0",'Pozitif genel çözümü ve y(1) = e koşulunu sağlayan çözümü bulun. Genel çözümün elde edilmesi sırasında dışarıda kalabilecek çözüm olup olmadığını belirtin.')
work_space(150)
question(2,r"y''-2y'+y=e^{\lambda x},\qquad y(0)=y'(0)=0,\quad\lambda\in\mathbb{R}",'Çözümü λ = 1 ve λ ≠ 1 için bulun. λ ≠ 1 için bulduğunuz ifadenin λ → 1 limitini hesaplayın ve iki sonucun tutarlılığını değerlendirin.')
work_space(150)

page('Sorular | 3-4','Tanım bölgesi ve çözümün sürdürülmesi')
question(3,r"(1-x^2)y''-2xy'+2y=0",'x = 0 ve x = 1 noktalarını sınıflandırın. Denklemin y = x çözümünü de kontrol ederek “x = 1 tekil olduğuna göre hiçbir çözüm o noktada analitik olamaz” iddiasını değerlendirin.')
work_space(150)
question(4,r"x+yy'=0,\qquad y(0)=1",'Başlangıç değer problemini ve x = 0’ı içeren en geniş çözüm aralığını bulun. Çözümü temsil eden kapalı eğrinin diğer dalını seçerek aynı y(x) çözümünü aralığın uçlarından geçirmek mümkün müdür? Gerekçelendirin.')
work_space(150)

page('Sorular | 5-6','Tam çözüm ve seri merkezi')
question(5,r"y'''-y'=2x,\qquad y(0)=y'(0)=y''(0)=0",'Başlangıç değer problemini çözün. Çözümün ilk sıfır olmayan Taylor terimini ve x → +∞ davranışını belirtin.')
work_space(150)
question(6,r"y''+(x-1)y'+y=0,\qquad y(1)=0,\quad y'(1)=1",'x = 1 etrafındaki seri çözüm için yineleme bağıntısını ve ilk dört sıfır olmayan terimi bulun.')
work_space(150)

page('Sorular | 7-8','Başlangıç koşulu ve teklik')
question(7,r"y'=y^2-2xy+x^2+1,\qquad y(0)=0",'Denklemin y = x çözümü bilinmektedir. Bir çözüm denemesinin başlangıç koşulunu sağlayamaması, bu başlangıç değer probleminin çözümsüz olduğunu gösterir mi? Çözümü bulun ve tekliğini değerlendirin.')
work_space(150)
question(8,r"x^2y''-3xy'+4y=0,\qquad x>0",'lim(x→0⁺) y(x) = 0 ve lim(x→0⁺) y′(x) = 0 koşullarını sağlayan bütün çözümleri bulun. İki koşulun neden tek bir çözüm seçip seçmediğini açıklayın.')
work_space(150)

page('Sorular | 9-10','Bağımsız çözümler ve değişken katsayılar')
question(9,r"x^2y''+xy'+\left(x^2-\frac14\right)y=0,\qquad x>0",'x = 0 etrafındaki indis köklerini ve iki bağımsız çözümün ilk üç sıfır olmayan terimini bulun. Küçük kökte serbest kalan bir katsayı varsa bunun bağımsız çözüm seçimine etkisini açıklayın. İkinci çözümde logaritma gerekli midir?')
work_space(145)
question(10,r"x^2y''-2xy'+2y=\frac{x}{1+x},\qquad x>0",'Genel çözümü bulun.')
work_space(145)

page('Sorular | 11-12','Uzun dönem davranışı ve parametreye bağlı çözüm yapısı')
question(11,r"y''+4y=\cos2x+\cos3x,\qquad y(0)=y'(0)=0",'Çözümü bulun. x ≥ 0 için sınırlı olup olmadığını gerekçelendirin.')
work_space(150)
question(12,r"x^2y''-xy'+(\alpha x-x^2)y=0,\qquad x>0,\quad\alpha\in\mathbb{R}",'x = 0 etrafındaki indis köklerini bulun. İki bağımsız çözümün de logaritmasız Frobenius serisi olmasına izin veren α değerlerini belirleyin. Kararı katsayı denklemleriyle gerekçelendirin; tam genel çözüm istenmiyor.')
work_space(150)

save('MAT501_Karisik_Genel_Tekrar_01.pdf','MAT501 - Karışık Genel Tekrar 01','Yeni karışık alıştırmalar')
(TMP/'general_review_equations.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
