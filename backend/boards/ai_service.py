import google.generativeai as genai

def generate_card_description(title):
    # 👇 Senin şifren burada kalsın
    MY_API_KEY = "AIzaSyD6Q-fLpMdwUKAW515Pp7LvLOt22AjoIhc"

    try:
        genai.configure(api_key=MY_API_KEY)
        
        # 🔄 GÜNCELLEME: 'gemini-flash-latest' kullanıyoruz.
        # Bu, kotası en yüksek ve en stabil ücretsiz modeldir.
        model = genai.GenerativeModel('gemini-flash-latest') 
        
        prompt = f"""
        Sen profesyonel bir proje yöneticisisin. 
        '{title}' başlıklı görev için yazılımcılara yönelik teknik bir açıklama (Acceptance Criteria) yaz.
        Türkçe cevap ver.
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini Hatası: {str(e)}"