import urllib.request
import xml.etree.ElementTree as ET
import os
import re
import time
from deep_translator import GoogleTranslator

# Registrar namespaces comunes en RSS
ET.register_namespace('media', 'http://search.yahoo.com/mrss/')
ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')

# Fuentes de noticias (Canonical Blog + Discourse News)
SOURCES = [
    {"name": "Ubuntu Blog", "url": "https://ubuntu.com/blog/feed", "tag": "canonical"},
    {"name": "Discourse News", "url": "https://discourse.ubuntu.com/c/news/40.rss", "tag": "discourse"}
]

OUTPUT_DIR = os.path.join("content", "noticias")

def translate_text(text, target='es'):
    if not text: return ""
    try:
        # Pausa para evitar rate-limiting
        time.sleep(0.5)
        return GoogleTranslator(source='auto', target=target).translate(text)
    except Exception as e:
        print(f"Error traduciendo: {e}")
        return text

def clean_html(raw_html):
    if not raw_html: return ""
    # Remueve etiquetas HTML y decodifica entidades básicas
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def extract_image(item, description):
    # 1. Intentar con media:content (vía ET con namespace)
    media = item.find('{http://search.yahoo.com/mrss/}content')
    if media is not None and 'url' in media.attrib:
        return media.attrib['url']
        
    # 2. Intentar con enclosure
    enclosure = item.find('enclosure')
    if enclosure is not None and 'url' in enclosure.attrib:
        return enclosure.attrib['url']
        
    # 3. Fallback: buscar img en la descripción (estilo robusto)
    # Buscamos la primera URL que parezca una imagen (jpg, png, webp, gif)
    img_match = re.search(r'https?://[^\s<>"]+?\.(?:jpg|jpeg|png|webp|gif)', description)
    if img_match:
        return img_match.group(0)

    # 4. Fallback: buscar img tag
    img_tag_match = re.search(r'<img [^>]*src="([^"]+)"', description)
    if img_tag_match:
        return img_tag_match.group(1)
        
    return ""

def fetch_rss():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for source in SOURCES:
        print(f"\n--- Procesando: {source['name']} ({source['url']}) ---")
        
        req = urllib.request.Request(source['url'], headers={'User-Agent': 'Mozilla/5.0'})
        
        try:
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
            root = ET.fromstring(xml_data)
        except Exception as e:
            print(f"Error al conectar con {source['name']}: {e}")
            continue
            
        nuevas_noticias = 0
        # Iterar solo por las últimas 5 publicaciones de cada fuente
        for item in root.findall('./channel/item')[:5]:
            title_en = item.find('title').text
            link = item.find('link').text
            pubDate = item.find('pubDate').text
            description_elem = item.find('description')
            description = description_elem.text if description_elem is not None else ""
            
            # Extraer imagen
            thumbnail = extract_image(item, description)
            
            # Extraer Categorías/Tags del RSS
            tags = [source['tag']]
            for cat in item.findall('category'):
                if cat.text:
                    tags.append(cat.text.lower().replace(' ', '-'))
            
            # Limpiar y preparar resumen
            summary_en = clean_html(description)[:250] + "..."
            
            # Generar "Slug" único por fuente para evitar colisiones
            slug_base = re.sub(r'[^a-zA-Z0-9]', '-', title_en.lower())
            slug = re.sub(r'-+', '-', slug_base).strip('-')
            filename = f"{source['tag']}-{slug}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Si el archivo ya existe, ignorarla (pero podrías actualizar la imagen si quisieras)
            if os.path.exists(filepath):
                continue
                
            # Traducir a español
            print(f"Traduciendo: {title_en[:40]}...")
            title = translate_text(title_en)
            summary = translate_text(summary_en)

            print(f"Guardando: {title}")
            
            # Frontmatter de Hugo
            content = f"""---
title: "{title.replace('"', "'")}"
date: "{pubDate}"
type: "noticias"
source: "{source['name']}"
thumbnail: "{thumbnail}"
tags: {tags}
---
> **Aviso de Importación Automática ({source['name']})**

{summary}

<br>
<a href="{link}" target="_blank" class="p-button--positive">Ver publicación original en {source['name']}</a>
"""
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            nuevas_noticias += 1

        if nuevas_noticias == 0:
            print(f"No hay noticias nuevas en {source['name']}.")
        else:
            print(f"Completado: Se generaron {nuevas_noticias} nuevas noticias de {source['name']}.")

if __name__ == "__main__":
    fetch_rss()
