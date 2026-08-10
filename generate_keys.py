"""Generar un set completo de iconos de teclas de teclado en estilo keycap.

El estilo replica una referencia visual: doble contorno (exterior grueso,
interior fino) simulando el bisel de una tecla física, esquinas redondeadas,
y una etiqueta centrada en negro sobre fondo transparente.
"""

import os
import cairosvg
# Dependencia: Requiere la librería nativa 'cairo' instalada en el sistema 
# (ej. GTK3-Runtime en Windows) para realizar la conversión a PNG.

OUTPUT_SVG_DIR = "svg"
OUTPUT_PNG_DIR = "png"
CANVAS = 200
OUTER_STROKE = 14
INNER_STROKE = 6
INNER_MARGIN = 26
OUTER_RADIUS = 24
INNER_RADIUS = 14


def escape_xml(text: str) -> str:
    """Escapar caracteres reservados de XML (<, >, &) para uso seguro en SVG."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(label: str, font_size: int, color: str = "black") -> str:
    """Construir el markup SVG de una tecla con doble contorno y etiqueta centrada."""
    inner_x = INNER_MARGIN
    inner_y = INNER_MARGIN
    inner_size = CANVAS - 2 * INNER_MARGIN
    center = CANVAS / 2
    label = escape_xml(label)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}">
  <rect x="{OUTER_STROKE / 2}" y="{OUTER_STROKE / 2}"
        width="{CANVAS - OUTER_STROKE}" height="{CANVAS - OUTER_STROKE}"
        rx="{OUTER_RADIUS}" fill="none" stroke="{color}" stroke-width="{OUTER_STROKE}"/>
  <rect x="{inner_x}" y="{inner_y}" width="{inner_size}" height="{inner_size}"
        rx="{INNER_RADIUS}" fill="none" stroke="{color}" stroke-width="{INNER_STROKE}"/>
  <text x="{center}" y="{center}" font-family="Arial, Helvetica, sans-serif"
        font-weight="bold" font-size="{font_size}" fill="{color}"
        text-anchor="middle" dominant-baseline="central">{label}</text>
</svg>"""


AVG_CHAR_WIDTH_FACTOR = 0.62
USABLE_WIDTH = CANVAS - 2 * INNER_MARGIN - 12


def font_size_for(label: str) -> int:
    """Calcular el tamaño de fuente máximo que cabe dentro del borde interior."""
    if len(label) == 1:
        return 90
    max_by_width = int(USABLE_WIDTH / (len(label) * AVG_CHAR_WIDTH_FACTOR))
    return min(64, max_by_width)


def build_key_set() -> dict:
    """Definir el conjunto completo de teclas: letras, números, función y modificadores."""
    keys = {}

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        keys[letter] = letter

    for digit in "0123456789":
        keys[digit] = digit

    for n in range(1, 13):
        name = f"F{n}"
        keys[name] = name

    modifiers = [
        "Ctrl", "Alt", "AltGr", "Shift",  "Win", "Fn",
        "Enter", "Intro", "Esc", "Tab", "Space", "Backspace", "Delete",
        "CapsLock", "NumLock", "Home", "End", "PgUp", "PgDn", "Insert",
        "PrtSc",
    ]
    for m in modifiers:
        keys[m] = m

    symbols = {
        "plus": "+",
        "minus": "-",
        "lt_gt": "<>",
        "period": ".",
        "comma": ",",
        "ene_ntilde": "Ñ",
        "up": "↑", 
        "down": "↓", 
        "Left": "←",
        "Right": "→",
    }
    keys.update(symbols)

    return keys


def sanitize_filename(name: str) -> str:
    """Convertir la etiqueta en un nombre de archivo seguro y en minúsculas."""
    return name.lower().replace(" ", "_")


def main():
    key_set = build_key_set()

    variants = {"black": "black", "white": "white", "brand_blue": "#1392ec"}

    for variant_name, color in variants.items():
        svg_dir = os.path.join(OUTPUT_SVG_DIR, variant_name)
        png_dir = os.path.join(OUTPUT_PNG_DIR, variant_name)
        os.makedirs(svg_dir, exist_ok=True)
        os.makedirs(png_dir, exist_ok=True)

        for key, label in key_set.items():
            filename = sanitize_filename(key)
            svg_content = build_svg(label, font_size_for(label), color=color)

            svg_path = os.path.join(svg_dir, f"{filename}.svg")
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

            png_path = os.path.join(png_dir, f"{filename}.png")
            cairosvg.svg2png(
                url=svg_path,
                write_to=png_path,
                output_width=400,
                output_height=400,
                background_color=None,
            )

    print(f"Generadas {len(key_set)} teclas x {len(variants)} variantes de color")


if __name__ == "__main__":
    main()
