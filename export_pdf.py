from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def _shorten_display_link(url, max_len=40):
    """Devuelve una versión visual corta del link (pero se mantiene el href completo)."""

    if len(url) <= max_len:
        return url
    return url[: max_len - 3] + "..."


def export_to_pdf(data, filename="resultados.pdf"):

    if not data:
        print("No hay datos para exportar.")
        return

    # Márgenes en pulgadas (puedes ajustar)
    left_margin = right_margin = 0.6 * inch
    top_margin = bottom_margin = 0.5 * inch

    # Página en horizontal
    page_size = landscape(letter)
    page_width, page_height = page_size

    # Documento
    doc = SimpleDocTemplate(
        filename,
        pagesize=page_size,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Estilos personalizados (ajusta fontSize y leading si quieres)
    styles.add(ParagraphStyle(name="Small", fontSize=9, leading=11))
    styles.add(
        ParagraphStyle(name="Link", textColor=colors.blue, fontSize=9, leading=11)
    )
    styles.add(ParagraphStyle(name="Resumen", fontSize=9, leading=12))
    styles.add(ParagraphStyle(name="TituloCell", fontSize=10, leading=12))

    # Título
    title = Paragraph("Resultados de Búsqueda Académica", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Encabezados y filas como Paragraphs para permitir wrap
    headers = list(data[0].keys())
    rows = []

    # Primera fila: encabezados (usar estilo negrita)
    header_row = []
    for h in headers:
        header_row.append(Paragraph(str(h), styles["Normal"]))
    rows.append(header_row)

    # Filas de contenido
    for item in data:
        row = []
        for key in headers:
            value = item.get(key, "")
            key_lower = str(key).lower()
            if key_lower == "link":
                display = _shorten_display_link(str(value), max_len=50)
                # enlazar (<a href="...">display</a>) — algunos visores PDF respetan enlaces
                cell = Paragraph(f'<a href="{value}">{display}</a>', styles["Link"])
            elif key_lower == "resumen" or key_lower == "abstract":
                cell = Paragraph(str(value), styles["Resumen"])
            elif key_lower == "título" or key_lower == "titulo" or key_lower == "title":
                cell = Paragraph(str(value), styles["TituloCell"])
            else:
                cell = Paragraph(str(value), styles["Small"])
            row.append(cell)
        rows.append(row)

    # Calcular ancho disponible y asignar proporciones
    available_width = page_width - left_margin - right_margin

    # Proporciones (ajusta según tus columnas: Fuente, Título, Resumen, Link)
    # Asegúrate que la longitud de col_ratios coincida con el número de columnas
    n_cols = len(headers)
    # Ejemplo por defecto para 4 columnas: [Fuente, Título, Resumen, Link]
    if n_cols == 4:
        col_ratios = [0.12, 0.25, 0.48, 0.15]
    else:
        # Si el número de columnas cambia, repartir proporcionalmente
        base = 1.0 / n_cols
        col_ratios = [base] * n_cols

    # Convertir ratios a anchos reales
    col_widths = [available_width * r for r in col_ratios]

    # Asegurarse que la suma sea exactamente available_width (pequeña corrección)
    total = sum(col_widths)
    if total != available_width:
        diff = available_width - total
        col_widths[-1] += diff

    # Crear la tabla
    table = Table(rows, colWidths=col_widths, repeatRows=1)

    # Estilo de la tabla
    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#8D8D8D"),
                ),  # header grey
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                # Celdas
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
            ]
        )
    )

    elements.append(table)
    doc.build(elements)

    print(f"\n✅ PDF generado correctamente: {filename}\n")
