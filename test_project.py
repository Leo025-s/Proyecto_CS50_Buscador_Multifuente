from project import search_all_sources, search_arxiv, search_crossref, search_openalex
import pytest


def test_search_all_sources():

    topic = "Inteligencia Artificial"
    results = search_all_sources(topic)

    assert isinstance(results, list), "search_all_sources() debe devolver una lista"
    assert (len(results) > 0), "La lista de resultados está vacía, debería contener al menos un resultado"

    for i, item in enumerate(results, start=1):

        assert isinstance(item, dict), f"El resultado #{i} no es un diccionario"
        assert "Título" in item, f"Falta la clave 'Título' en el resultado #{i}"
        assert "Fuente" in item, f"Falta la clave 'Fuente' en el resultado #{i}"
        assert "Resumen" in item, f"Falta la clave 'Resumen' en el resultado #{i}"
        assert "Link" in item, f"Falta la clave 'Link' en el resultado #{i}"

def test_search_crossref():
    topic = "Machine Learning"
    results = search_crossref(topic)

    assert isinstance(results, list), "search_crossref() debe devolver una lista"
    assert len(results) > 0, "search_crossref() devolvió una lista vacía"

    for i, item in enumerate(results, start=1):
        assert isinstance(item, dict), f"El resultado #{i} no es un diccionario"
        assert "Título" in item, f"Falta la clave 'Título' en el resultado #{i}"
        assert "Fuente" in item, f"Falta la clave 'Fuente' en el resultado #{i}"
        assert "Resumen" in item, f"Falta la clave 'Resumen' en el resultado #{i}"
        assert "Link" in item, f"Falta la clave 'Link' en el resultado #{i}"

def test_search_openalex():
    topic = "Data Science"
    results = search_openalex(topic)

    assert isinstance(results, list), "search_openalex() debe devolver una lista"
    assert len(results) > 0, "search_openalex() devolvió una lista vacía"

    for i, item in enumerate(results, start=1):
        assert isinstance(item, dict), f"El resultado #{i} no es un diccionario"
        assert "Título" in item, f"Falta la clave 'Título' en el resultado #{i}"
        assert "Fuente" in item, f"Falta la clave 'Fuente' en el resultado #{i}"
        assert "Resumen" in item, f"Falta la clave 'Resumen' en el resultado #{i}"
        assert "Link" in item, f"Falta la clave 'Link' en el resultado #{i}"

def test_search_arxiv():
    topic = "Inteligencia Artificial"
    results = search_arxiv(topic)

    assert isinstance(results, list), "search_arxiv() debe devolver una lista"
    assert len(results) > 0, "search_arxiv() devolvió una lista vacía"

    for i, item in enumerate(results, start=1):
        assert isinstance(item, dict), f"El resultado #{i} no es un diccionario"
        assert "Título" in item, f"Falta la clave 'Título' en el resultado #{i}"
        assert "Fuente" in item, f"Falta la clave 'Fuente' en el resultado #{i}"
        assert "Resumen" in item, f"Falta la clave 'Resumen' en el resultado #{i}"
        assert "Link" in item, f"Falta la clave 'Link' en el resultado #{i}"