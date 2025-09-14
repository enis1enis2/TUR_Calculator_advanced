# Import / İçe Aktarma
from flask import Flask, render_template, request

app = Flask(__name__)

# Enerji hesaplama fonksiyonu
def result_calculate(size, lights, device):
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5   
    return size * home_coef + lights * light_coef + device * devices_coef 

# ----------------------------
# Ana Sayfa (Ev büyüklüğü seçimi)
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------------------
# Lamba sayısı seçimi
# ----------------------------
@app.route('/<int:size>')
def lights_page(size):
    return render_template('lights.html', size=size)

# ----------------------------
# Elektrikli cihaz sayısı seçimi
# ----------------------------
@app.route('/<int:size>/<int:lights>')
def electronics_page(size, lights):
    return render_template('electronics.html', size=size, lights=lights)

# ----------------------------
# Hesaplama ve Sonuç
# ----------------------------
@app.route('/<int:size>/<int:lights>/<int:device>')
def end(size, lights, device):
    result = result_calculate(size, lights, device)
    # Pass answers via query parameters to the form link
    return render_template('end.html', size=size, lights=lights, device=device, result=result)

# ----------------------------
# Form Sayfası
# ----------------------------
@app.route('/form/<size>/<lights>/<device>/<result>')
def form(size, lights, device, result):
    return render_template('form.html', size=size, lights=lights, device=device, result=result)

# ----------------------------
# Form submit işlemi
# ----------------------------
@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']
    size_code = request.form.get('size')
    lights_code = request.form.get('lights')
    device = request.form.get('device')
    result = request.form.get('result')

    # Kod -> Metin dönüşümleri
    size_map = {'1': 'Küçük', '2': 'Orta', '3': 'Büyük'}
    lights_map = {'1': '2-4 lamba', '2': '4-6 lamba', '3': '8+ lamba'}

    size_text = size_map.get(size_code, 'N/A')
    lights_text = lights_map.get(lights_code, 'N/A')

    # cevap.txt dosyasına kaydet
    with open('cevap.txt', 'a', encoding='utf-8') as f:
        f.write(
            f"Ad: {name}\n"
            f"E-posta: {email}\n"
            f"Adres: {address}\n"
            f"Tarih: {date}\n"
            f"Evin büyüklüğü: {size_text}\n"
            f"Lamba sayısı: {lights_text}\n"
            f"Cihaz sayısı: {device}\n"
            f"Enerji sonucu: {result} kWh\n"
            "-------------------------------------\n"
        )

    # -> Burada artık redirect yok, direkt sonucu gösteriyoruz
    return render_template('form_result.html',
                           name=name,
                           email=email,
                           address=address,
                           date=date,
                           size=size_text,
                           lights=lights_text,
                           device=device,
                           result=result)
@app.route('/solutions')
def solutions():
    suggestions = [
        "LED ampullere geçin (klasik ampullere göre %80 daha az enerji).",
        "Kullanılmayan cihazların fişini çekin (stand-by modu bile enerji tüketir).",
        "Enerji verimli (A++ veya üstü) beyaz eşyalar kullanın.",
        "Gündüz doğal ışığı kullanın, gündüz perdeleri açık tutun.",
        "Ev yalıtımını iyileştirerek ısı kaybını azaltın.",
        "Akıllı prizler kullanarak cihazları zamanlayın.",
        "Enerji tasarruflu klima ve ısıtıcılar tercih edin.",
        "Çamaşırları düşük sıcaklıkta ve tam yükte yıkayın.",
        "Gereksiz aydınlatmaları kapatmayı alışkanlık haline getirin.",
        "Güneş paneli gibi yenilenebilir enerji kaynaklarını değerlendirin."
    ]
    return render_template('solutions.html', suggestions=suggestions)

# ----------------------------
# Uygulamayı çalıştır
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
