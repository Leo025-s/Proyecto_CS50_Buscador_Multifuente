from googletrans import Translator
import re

translator = Translator()

# Función Traducir
def translate_summary(summary):
    try:
        detection = translator.detect(summary)
        if detection.lang == "en":
            translated = translator.translate(summary, src="en", dest="es")
            return translated.text
        return summary
    except Exception as e:
        print(f"[warning] Error traduciendo resumen: {e}")
        return summary


# Función Reconstruir resumen (para OpenAlex)
def rebuild_summary_OpenAlex(summary):

    if not summary:
        return "(Sin resumen disponible)"  # <-- devuelve texto, no None

    palabras = sorted(
        [(pos, palabra)
         for palabra, posiciones in summary.items()
         for pos in posiciones]
    )
    return " ".join([p[1] for p in palabras])

# Función Reconstruir resumen (para Crossref)
def rebuild_summary_Crossref(summary):

    if not summary:
        return "(Sin resumen disponible)"
    
    if isinstance(summary, str):
        clean_abstract = re.sub(r'<jats:[^>]*>|&lt;/?jats:[^&gt;]*&gt;', '', summary, flags=re.IGNORECASE)
        clean_abstract = re.sub(r'<[^>]*>', '', clean_abstract) 
        
        cleaned_text = clean_abstract.strip()
        # Opcional: truncar el resumen
        return cleaned_text if len(cleaned_text) <= 300 else cleaned_text[:300] + "..."
    
    return "(Error de formato de resumen desconocido)"