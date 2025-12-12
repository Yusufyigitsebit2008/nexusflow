import google.generativeai as genai
from django.conf import settings

def generate_card_description(title):
    """
    Verilen başlığa göre Gemini API kullanarak profesyonel iş tanımı oluşturur.
    """
    
    if not settings.GEMINI_API_KEY:
        return "⚠️ API Key bulunamadı. .env dosyasını kontrol et."

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Daha stabil olan modeli seçiyoruz
        model = genai.GenerativeModel('gemini-flash-latest')

        # Prompt'u "Rol Yapma (Roleplay)" tekniği ile güçlendiriyoruz
        prompt = f"""
        Sen kıdemli bir Proje Yöneticisisin (Senior Project Manager).
        Aşağıdaki görev başlığı için yazılım ekibine atanacak profesyonel, net ve teknik bir görev açıklaması yaz.

        Kurallar:
        1. Cevabın TAMAMEN Türkçe olsun.
        2. Asla "Görev Başlığı" veya "Açıklama" gibi ana başlıkları tekrar etme. Direkt içeriğe başla.
        3. Markdown formatı kullan (Bold, Bullet point).
        4. İçeriği şu 3 alt başlığa böl:
           - 🎯 **Özet** (1 cümle)
           - 📋 **Gereksinimler** (Maddeler halinde)
           - ✅ **Kabul Kriterleri** (Definition of Done)

        Görev Başlığı: {title}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"🔴 Gemini AI Hatası: {str(e)}")
        return "Yapay zeka şu an çok yoğun. Lütfen açıklamayı manuel gir."