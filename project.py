import pyfiglet
import time
import requests
from tabulate import tabulate
from urllib.parse import quote_plus
from xml.etree import ElementTree
from utils import translate_summary, rebuild_summary_OpenAlex, rebuild_summary_Crossref
from export_pdf import export_to_pdf


# Función Principal (Main)
def main():

    texto = "Buscador Académico Multipfuente"
    fuente = "cursive"
    arte_ascii = pyfiglet.figlet_format(texto, font=fuente, width=120, justify="center")
    print(arte_ascii)

    topic = input("Ingrese el tema que desea buscar: ").strip()

    result = search_all_sources(topic)

    if result:
        print("\nResultados Encontrados:\n")
        print(tabulate(result, headers="keys", tablefmt="fancy_grid"))

        opcion = input("\n¿Desea guardar los resultados en un PDF? (s/n): ").strip().lower()
        if opcion == "s":
            export_to_pdf(result, filename="resultados.pdf")
    else:
        print("No se encontraron resultados para esta busqueda.")
# ============================================================================


# ========================
#   Funcipon buscar en arXiv  ================================================
def search_arxiv(query, max_results=5, delay=0.5):
    
    if not query:
        return []

    escaped = quote_plus(query)

    url = f"http://export.arxiv.org/api/query?search_query=all:{escaped}&max_results={max_results}"

    time.sleep(delay)

    resp = requests.get(
        url, headers={"User-Agent": "AcademicFinder/1.0 (CS50 project)"}
    )

    if resp.status_code != 200:
        raise ConnectionError(f"arXiv responded with status {resp.status_code}")

    root = ElementTree.fromstring(resp.content)
    namespace = "{http://www.w3.org/2005/Atom}"
    results = []

    for entry in root.findall(f"{namespace}entry"):

        title_el = entry.find(f"{namespace}title")
        title = title_el.text.strip() if title_el is not None and title_el.text else "Sin título"

        id_el = entry.find(f"{namespace}id")
        link = id_el.text.strip() if id_el is not None and id_el.text else ""

        summary_el = entry.find(f"{namespace}summary")
        summary = summary_el.text.strip() if summary_el is not None and summary_el.text else ""

        summary = translate_summary(summary)

        short_summary = (summary[:300] + "...") if len(summary) > 300 else summary

        results.append({

            "Fuente": "arXiv",
            "Título": title,
            "Resumen": short_summary,
            "Link": link
        })
    
    return results 
# ===========================================================================


# ==========================
#   Función buscar en OpenAlex ==============================================
def search_openalex(query, max_results=5, delay=0.5):

    if not query:
        return []

    escaped = quote_plus(query)

    url = f"https://api.openalex.org/works?search={escaped}&per-page={max_results}"
    time.sleep(delay)
    resp = requests.get(url, headers={"User-Agent": "AcademicFinder/1.0 (CS50 project)"})

    if resp.status_code != 200:
        raise ConnectionError(f"OpenAlex responded with status {resp.status_code}")

    data = resp.json()
    results = []

    for i, work in enumerate(data["results"], start=1):

        title = work.get("display_name") or "Sin título"

        link = work.get("doi") or work.get("id") or "Enlace no disponible"

        summary = rebuild_summary_OpenAlex(work.get("abstract_inverted_index"))

        summary = translate_summary(summary)

        short_summary = (summary[:300] + "...") if len(summary) > 300 else summary

        results.append({

            "Fuente": "OpenAlex",
            "Título": title,
            "Resumen": short_summary,
            "Link": link
        })
    
    return results
# ===========================================================================

# ==========================
#   Función buscar en Crossref ==============================================
def search_crossref(query, max_results=5, delay=0.5):

    if not query:
        return []

    escaped = quote_plus(query)

    url = f"https://api.crossref.org/works?query={escaped}&rows={max_results}"
    time.sleep(delay)
    resp = requests.get(url, headers={"User-Agent": "AcademicFinder/1.0 (CS50 project)"})

    if resp.status_code != 200:
        raise ConnectionError(f"Crossref responded with status {resp.status_code}")

    data = resp.json()
    results = []

    for i, work in enumerate(data["message"]["items"], start=1):

        title_list = work.get("title")

        if title_list and isinstance(title_list, list) and len(title_list) > 0:
            # Si es una lista, toma el primer elemento (el título real)
            title = title_list[0]
        else:
            # Si está vacío o no es una lista, usa el valor por defecto
            title = "Sin título"

        link = work.get("URL") or work.get("DOI") or "Enlace no disponible"

        summary = rebuild_summary_Crossref(work.get("abstract"))

        summary = translate_summary(summary)

        short_summary = (summary[:300] + "...") if len(summary) > 300 else summary

        results.append(
            {
                "Fuente": "Crossref",
                "Título": title,
                "Resumen": short_summary,
                "Link": link,
            }
        )
    
    return results
# ===========================================================================

# ===================================
# Función buscar en todas las fuentes =======================================
def search_all_sources(topic):
    results = []

    results += search_arxiv(topic)
    results += search_openalex(topic)
    results += search_crossref(topic)
    

    return results
# ========================================================================



if __name__ == "__main__":
    main()
