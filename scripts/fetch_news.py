import urllib.request
import xml.etree.ElementTree as ET
import os
import re
import time
from deep_translator import GoogleTranslator

RSS_URL = "https://ubuntu.com/blog/feed"
OUTPUT_DIR = os.path.join("content", "noticias")

def translate_text(text, target='es'):
    try:
        # Pausa para evitar rate-limiting
        time.sleep(1)
        return GoogleTranslator(source='en', target=target).translate(text)
    except Exception as e:
        print(f"Error traduciendo: {e}")
        return text

def clean_html(raw_html):
    # Remueve etiquetas HTML del resumen de la noticia
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def fetch_rss():
    print(f"Buscando noticias oficiales en {RSS_URL}...")
    
    # Fake User-Agent para evitar bloqueos del servidor de Canonical
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
    except Exception as e:
        print(f"Error al conectar con el RSS: {e}")
        return
    
    root = ET.fromstring(xml_data)
    
    # Crear carpeta de noticias en Hugo si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    nuevas_noticias = 0
    # Iterar solo por las últimas 5 publicaciones
    for item in root.findall('./channel/item')[:5]:
        title_en = item.find('title').text
        link = item.find('link').text
        pubDate = item.find('pubDate').text
        description = item.find('description').text
        
        # Limpiar el HTML basura y traducir resumen
        summary_en = clean_html(description)[:250] + "..."
        
        # Traducir a español
        print(f"Traduciendo: {title_en[:30]}...")
        title = translate_text(title_en)
        summary = translate_text(summary_en)

        # Generar "Slug"
        slug = re.sub(r'[^a-zA-Z0-9]', '-', title_en.lower())
        slug = re.sub(r'-+', '-', slug).strip('-')
        filename = f"{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Si el archivo ya existe, ignorarla
        if os.path.exists(filepath):
            continue
            
        print(f"Guardando noticia: {title}")
        
        # Frontmatter de Hugo
        content = f"""---
title: "{title.replace('"', "'")}"
date: "{pubDate}"
type: "noticias"
source: "Ubuntu Oficial"
tags: ["canonical", "importado-rss"]
---
> **Aviso de Importación Automática**

{summary}

<br>
<a href="{link}" target="_blank" class="p-button--positive">Leer noticia completa en el Blog de Ubuntu (Inglés)</a>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        nuevas_noticias += 1

    if nuevas_noticias == 0:
        print("No hay noticias nuevas para importar.")
    else:
        print(f"Completado: Se generaron {nuevas_noticias} noticias en {OUTPUT_DIR}.")

if __name__ == "__main__":
    fetch_rss()
