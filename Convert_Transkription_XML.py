#!/usr/bin/env python
# coding: utf-8

# # Convert Transkription to XML

# In[8]:


import os,glob,re
data_dir = os.path.expanduser('PATH_TO_DIR/*.txt')
data_paths = glob.glob(data_dir)

for file in sorted(data_paths):
    print(file)
    content = open(file).read()
    book = re.search(r'TEXT: (.+?)\n', content)
    ms = re.search(r'HS: ([\w\s()\.]+?)\n', content)
    initial_page = re.search(r'\(([0-9rv]+?)\)', content)
    #comment = re.search(r'Anmerkung: (.+?)\n', content)
    content_new = re.sub(r'TEXT: .+?\n', r'', content) # Löschen
    content_new = re.sub(r'HS: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'PDF: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'\n\([0-9rv]+?\)', r'', content_new) # Löschen
    #content_new = re.sub(r'Anmerkung: .+?\n', r'', content_new) # Löschen
    print(book.group(1),ms.group(1),initial_page.group(1))
    with open("/PATH_TO_DIR/TEXT_ID-"+ms.group(1)+"-transcript.xml", "w") as f:    
        # Umbrüche
        #content_new = re.sub(r'\(([\w\d]+?)\)\n', r'', content_new) # Löschen
        content_new = re.sub(r' ///\(([\w\d]+?)\)\n', r' <pb n="\1"/> ', content_new)
        content_new = re.sub(r'///\(([\w\d]+?)\)\n', r'<pb n="\1" break="no"/>', content_new) # im Wort
        content_new = re.sub(r' //', r' <cb/> ', content_new)
        content_new = re.sub(r'//', r'<cb break="no"/>', content_new) # im Wort
        content_new = re.sub(r' /[^>\w]{1}', r' <lb/> ', content_new)
        content_new = re.sub(r'/[^>\w]{1}', r'<lb break="no"/>', content_new) # im Wort
        # Besondere Texte
        content_new = re.sub(r'3([\w\s]+?)~([1-4]{1})~3', r'<note place="margin_\2">\1</note>', content_new) # Marginalien; Nachbearbeitung bzgl. Positionsnummer:
        content_new = re.sub(r'<note place="margin_1">', r'<note place="top">', content_new)
        content_new = re.sub(r'<note place="margin_2">', r'<note place="bottom">', content_new)
        content_new = re.sub(r'<note place="margin_3">', r'<note place="margin_inner">', content_new)
        content_new = re.sub(r'<note place="margin_4">', r'<note place="margin_outer">', content_new)
        #content_new = re.sub(r'4([\w\s]+?)~-4', r'<del>\1</del>', content_new) # getilgter Text; Kurzschreibung # obsolete
        content_new = re.sub(r'(?<!~)4([s\D]+?)~([1-3]{1})~4', r'<del rend="\2">\1</del>', content_new) # getilgter Text; Nachbearbeitung bzgl. Art der Tilgung:
        content_new = re.sub(r'<del rend="1">', r'<del rend="erasure">', content_new)
        content_new = re.sub(r'<del rend="2">', r'<del rend="strikethrough">', content_new)
        content_new = re.sub(r'<del rend="3">', r'<del rend="expunction">', content_new)
        #content_new = re.sub(r'4([\w\s]+?)~([\w\s]+?)4', r'<subst><del>\1</del><add>\2</add></subst>', content_new) # Textersetzung; Kurzschriebung # obsolete
        content_new = re.sub(r'4([\s\D]+?)~([0-4]{1})~([\s\D]+?)~([0-3]{1})~4', r'<subst><del rend="\2">\1</del><add place="\4">\3</add></subst>', content_new) # Textersetzung
        content_new = re.sub(r'<del rend="0">', r'<del rend="marker">', content_new) # zu ersetzender Text mit Marker (sc. dotted obelus o.ä.) markiert
        content_new = re.sub(r'<del rend="1">', r'<del rend="erasure">', content_new)
        content_new = re.sub(r'<del rend="2">', r'<del rend="strikethrough">', content_new)
        content_new = re.sub(r'<del rend="3">', r'<del rend="expunction">', content_new)
        content_new = re.sub(r'<del rend="4">', r'<del rend="without">', content_new)
        #content_new = re.sub(r'5([\w\s]+?)5', r'<add>\1</add>', content_new) # Text über der Zeile; Kurzschreibung # obsolete
        content_new = re.sub(r'5([\w\s]+?)~([1-3]{1})~5', r'<add place="\2">\1</add>', content_new) # Text über der Zeile
        content_new = re.sub(r'<add place="1">', r'<add place="above">', content_new) # auch für Textersetzung
        content_new = re.sub(r'<add place="2">', r'<add place="inline">', content_new)
        content_new = re.sub(r'<add place="3">', r'<add place="margin">', content_new)
        content_new = re.sub(r'6...([0-9a-zA-Z]+?)...6', r'<gap reason="lost" quantity="\1" unit="character"/>', content_new) # Lücke im Text
        content_new = re.sub(r'7...([0-9a-zA-Z]+?)...7', r'<gap reason="illegible" quantity="\1" unit="character"/>', content_new) # Nicht lesbarer Text
        content_new = re.sub(r'8([\w\s@]+?)8', r'<unclear>\1</unclear>', content_new) # unsichere Lesung
        content_new = re.sub(r'9([\w]+?)~([\w]+?)9', r'<choice><expan>\2</expan><abbr type="nomSac"><hi rend="overline">\1</hi></abbr></choice>', content_new) # nomina sacra
        # Zitate
        content_new = re.sub(r'@@', r'<g type="doubled_diple"/>', content_new)
        content_new = re.sub(r'@ ', r'<g type="diple"/>', content_new)
        content_new = re.sub(r'— ', r'<g type="paragraphos"/>', content_new)
        # Initialen und Ektheseis
        content_new = re.sub(r'1([\D]+?)1', r'<hi rend="initial">\1</hi>', content_new)
        content_new = re.sub(r'2([\D]+?)2', r'<hi rend="ekthesis">\1</hi>', content_new)
        # Titel und Lemma
        title = re.search(r'(?<!\d)0(.+?)(?<!\d)0', content_new, flags=re.DOTALL)
        content_new = re.sub(r'(?<!\d)0(.+?)(?<!\d)0', r'', content_new, flags=re.DOTALL) # Löschen
        ## Ausdruck
       # XML-Grundgerüst
        print('''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title xml:lang="la">'''+book.group(1)+'''</title>
                <author>Theodoret</author>
            </titleStmt>
            <publicationStmt>
                <publisher>BBAW Bibelexegese</publisher>
                <idno type="filename">CPG6207-'''+ms.group(1)+'''-transcript.xml</idno>
            </publicationStmt>
            <sourceDesc>
                <msDesc>
                    <msIdentifier>
                        <settlement></settlement>
                        <repository></repository>
                        <idno>'''+ms.group(1)+'''</idno>
                        <altIdentifier type="diktyon">
                            <idno></idno>
                        </altIdentifier>
                    </msIdentifier>
                </msDesc>'''
          #    <note>'''+comment.group(1)+'''</note>
            '''</sourceDesc>
        </fileDesc>
        <revisionDesc>
            <change who="#SH" when="2020-01-21">Transkript der Handschrift.</change>
        </revisionDesc>
    </teiHeader>
    <text xml:lang="grc">
        <body>
            <div type="edition">
            <pb n="'''+initial_page.group(1)+'''"/><head><title>'''+title.group(1)+'''</title></head>
            <div type="textpart" subtype="chapter" n="1">
            <p>'''+content_new+'''</p>
                </div>
                </div>
        </body>
    </text>
</TEI>
    ''', file=f)


# In[ ]:





# In[ ]:
