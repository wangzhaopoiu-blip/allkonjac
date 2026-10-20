"""Render the reviewed comparison and its real language counterparts."""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

BASE = 'https://allkonjac.com'
SLUG = 'konjac-refined-powder-vs-konjac-gum'
DATE = '2026-10-20'
LABELS = {'en':'English', 'th':'ภาษาไทย', 'id':'Bahasa Indonesia'}

def path(lang, index=False):
    return ('' if lang == 'en' else '/' + lang) + '/blog/' + ('' if index else SLUG + '/')

def alternates(index=False):
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{path(lang,index)}">' for lang in LABELS) + f'<link rel="alternate" hreflang="x-default" href="{BASE}{path("en",index)}">'

def render(root, output):
    data = json.loads((root/'source/comparison/translation-input.json').read_text(encoding='utf-8'))
    maps = {'en':{u['id']:u['text'] for u in data['units']}}
    for lang in ('th','id'):
        maps[lang] = json.loads((root/f'source/comparison/{lang}.json').read_text(encoding='utf-8'))
        if set(maps[lang]) != set(maps['en']):
            raise ValueError('Incomplete comparison translation: '+lang)
    esc = html.escape
    for lang, values in maps.items():
        ui = {k:values[v] for k,v in data['ui'].items()}
        t = lambda k: esc(ui[k])
        body = data['template']
        for block in data['blocks']:
            key,tag = block['id'],block['tag']
            refs = ''.join(f' <a href="{r}" aria-label="{t("references")} {r[5:]}">[{r[5:]}]</a>' for r in block['refs'])
            translated = esc(values[key]).replace('*','') + refs
            pattern = rf'(<{tag}\b[^>]*data-unit="{key}"[^>]*>)[\s\S]*?(</{tag}>)'
            body,count = re.subn(pattern, lambda m:m[1]+translated+m[2], body, count=1)
            if count != 1: raise ValueError('Missing block '+key)
        body = re.sub(r' data-unit="U\d+"','',body)
        body = body.replace('>References</h2>', '>'+t('references')+'</h2><p>'+t('sourcescope')+'</p>')
        body = body.replace('Swipe or scroll the table to see all columns.',t('tablehint'))
        body = body.replace('aria-label="Comparison table"', 'aria-label="'+t('category')+'"')
        toc = ''.join(f'<a href="#{ident}">{label}</a>' for ident,label in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',body))
        switch = '<div class="comparison-languages">' + ' · '.join(f'<a lang="{l}" hreflang="{l}" href="{path(l)}"'+(' aria-current="page"' if l==lang else '')+'>'+label+'</a>' for l,label in LABELS.items())+'</div>'
        home = '/' if lang=='en' else '/'+lang+'/'
        nav = f'<header class="site-header"><div class="shell nav-wrap"><a class="brand" href="{home}"><img class="blog-wordmark" src="/assets/brand/all-konjac-wordmark.svg" alt="ALL KONJAC" width="180" height="26"></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="site-nav">{t("menu")} ☰</button><nav id="site-nav" class="site-nav"><a href="{path(lang,True)}">{t("journal")}</a><a href="{home}">{t("home")}</a><a class="nav-cta" href="{home}ingredients/">{t("ingredients")} ↗</a></nav></div></header>'
        footer = f'<footer class="site-footer"><div class="shell footer-grid"><div><div class="footer-brand">ALL KONJAC</div><p>{t("footer")}</p></div><div class="footer-links"><a href="{path(lang,True)}">{t("journal")}</a><a href="{home}#contact">{t("contact")} ↗</a></div></div></footer>'
        schema = {'@context':'https://schema.org','@type':'BlogPosting','headline':ui['title'],'description':ui['indexDeck'],'inLanguage':lang,'datePublished':DATE,'dateModified':DATE,'mainEntityOfPage':BASE+path(lang),'author':{'@type':'Organization','name':'ALL KONJAC','url':BASE+'/'},'publisher':{'@type':'Organization','name':'ALL KONJAC','url':BASE+'/'},'citation':re.findall(r'href="(https:[^"]+)"',body[body.index('id="references"'):])}
        def head(title, description, index=False):
            return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><title>{esc(title)} | ALL KONJAC</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{BASE}{path(lang,index)}">{alternates(index)}<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="{"website" if index else "article"}"><meta property="og:url" content="{BASE}{path(lang,index)}"><link rel="icon" href="/assets/brand/all-konjac-favicon.svg"><link rel="stylesheet" href="/assets/blog.css"><link rel="stylesheet" href="/assets/comparison.css"><script src="/assets/blog.js" defer></script></head><body>'
        steps = ''.join(f'<div><span>0{i}</span><div><strong>{t("step"+str(i))}</strong><small>{t("step"+str(i)+"note")}</small></div></div>' for i in range(1,4))
        # Preserve the approved English heading treatment.
        hero_title = t('title') if lang!='en' else 'Refined Konjac Powder <span class="h1-counterpart"><span class="versus">vs.</span> Konjac Gum:</span><span class="hero-subtitle"> Differences, Specifications and How to Choose</span>'
        page = head(ui['title'],ui['indexDeck']).replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script></head>')+nav
        page += f'<main id="main"><section class="comparison-hero"><div class="shell">{switch}<p class="eyebrow">{t("category")}</p><h1>{hero_title}</h1><p class="article-deck">{t("deck")}</p><div class="article-meta"><span>ALL KONJAC</span><span>·</span><span>{t("published")} <time datetime="{DATE}">{DATE}</time></span></div><div class="spec-route">{steps}</div></div></section><div class="shell article-layout comparison-layout"><aside class="article-sidebar"><nav class="toc-panel" aria-label="{t("toc")}"><p class="toc-title">{t("toc")}</p>{toc}</nav></aside><div class="article-main">{body}<div class="article-note">{t("note")}</div><div class="related-block"><span class="eyebrow">{t("related")}</span><a href="/blog/choose-konjac-powder-gum/">{t("enquiry")} ↗</a><a href="/blog/konjac-glucomannan-ingredient-selection-hydration-viscosity/">{t("research")} ↗</a></div><a class="back-link" href="{path(lang,True)}">← {t("back")}</a></div></div></main>{footer}</body></html>'
        output[path(lang).lstrip('/')+'index.html']=page
        card = f'<section class="comparison-feature"><div class="shell"><article class="comparison-feature-card"><div><p class="eyebrow">{t("newlabel")}</p><h2><a href="{path(lang)}">{t("title")}</a></h2><p>{t("indexDeck")}</p><a class="text-link" href="{path(lang)}">{t("read")} ↗</a></div><div class="comparison-feature-steps">'+''.join(f'<div><strong>{t("step"+str(i))}</strong><span>{t("step"+str(i)+"note")}</span></div>' for i in range(1,4))+'</div></article></div></section>'
        if lang == 'en':
            index = output['blog/index.html']
            index = index.replace('</head>',alternates(True)+'<link rel="stylesheet" href="/assets/comparison.css"></head>')
            index = index.replace('<section id="articles"',card+'<section id="articles"')
            index = index.replace('<main',switch.replace('href="/blog/'+SLUG+'/"','href="/blog/"').replace('/blog/'+SLUG+'/','/blog/')+'<main',1)
        else:
            index_switch = switch.replace('/blog/'+SLUG+'/','/blog/')
            index = head(ui['indexTitle'],ui['indexDeck'],True)+nav+f'<main id="main"><section class="comparison-hero"><div class="shell">{index_switch}<h1>{t("indexTitle")}</h1><p class="article-deck">{t("indexDeck")}</p></div></section>{card}</main>'+footer+'</body></html>'
        output[path(lang,True).lstrip('/')+'index.html']=index
    guide='blog/choose-konjac-powder-gum/index.html'
    output[guide]=output[guide].replace('<section class="blog-content-section blog-sources">',f'<section class="blog-content-section"><h2>Comparing refined powder and gum?</h2><p><a href="{path("en")}">Read the technical comparison of composition, test methods and food-trial criteria ↗</a></p></section><section class="blog-content-section blog-sources">')
    output['assets/comparison.css']=(root/'source/comparison/comparison.css').read_text(encoding='utf-8')+'\n@font-face{font-family:"Noto Sans Thai";src:url("/assets/fonts/NotoSansThai-variable.ttf") format("truetype");font-weight:100 900;font-display:swap}html[lang="th"] body{font-family:"Noto Sans Thai",Arial,sans-serif;line-height:1.85}html[lang="th"] .comparison-hero h1{font-size:clamp(32px,4.6vw,62px);line-height:1.35;letter-spacing:0}.comparison-languages{display:flex;justify-content:flex-end;gap:10px;padding:14px 26px;font-size:13px;flex-wrap:wrap}.comparison-languages a[aria-current="page"]{color:var(--green);font-weight:700}.related-block a{margin-top:14px}\n'
    ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
    xn='{http://www.w3.org/1999/xhtml}'
    sitemap=ET.fromstring(output['sitemap.xml'])
    existing={n.find(ns+'loc').text:n for n in sitemap}
    for index in (False,True):
        for lang in LABELS:
            url=BASE+path(lang,index)
            node=existing.get(url)
            if node is None:
                node=ET.SubElement(sitemap,ns+'url');ET.SubElement(node,ns+'loc').text=url
            for l in list(LABELS)+['x-default']:
                ET.SubElement(node,xn+'link',{'rel':'alternate','hreflang':l,'href':BASE+path('en' if l=='x-default' else l,index)})
    ET.indent(sitemap,space='  ')
    output['sitemap.xml']='<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(sitemap,encoding='unicode')+'\n'
    output['llms.txt']=output['llms.txt'].replace('six English blog URLs','the research journal and its available language counterparts')+'\n## Refined powder and gum comparison\n'+''.join(f'- [{LABELS[l]}]({BASE}{path(l)}): Composition, test methods and selection boundaries.\n' for l in LABELS)
