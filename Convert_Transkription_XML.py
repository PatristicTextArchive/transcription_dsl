#!/usr/bin/env python
# coding: utf-8

# # Convert Transkription to XML

# In[ ]:


import os,glob,re
# input needed here:
data_dir = os.path.expanduser('~/Downloads') # sources
xml_dir = os.path.expanduser('~/Downloads') # converted xml-files

data_paths = glob.glob(data_dir+"/*.txt")

for file in sorted(data_paths):
    print(file)
    content = open(file).read()
    text = re.search(r'TEXT: ([\w\s(),\.]+?)\n', content)
    ms = re.search(r'HS: ([\w\s]+?)_([\w\s]+?)_([\w\s]+?)_([\w\s]+?)\n', content)
    sigle = re.search(r'SIGLE: ([\w\s()\.]+?)\n', content)
    diktyon = re.search(r'DIKTYON: ([0-9]+?)\n', content)
    editor = re.search(r'EDITOR: ([\w\s]+?) \(([\w\s]+?)\)\n', content)
    date = re.search(r'DATUM: ([0-9\-]+?)\n', content)
    initial_page = re.search(r'\(([0-9rv]+?)\)', content)
    #comment = re.search(r'Anmerkung: (.+?)\n', content)
    content_new = re.sub(r'TEXT: .+?\n', r'', content) # Löschen
    content_new = re.sub(r'HS: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'SIGLE: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'EDITOR: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'PDF: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'online: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'SCAN: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'DIKTYON: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'DATUM: .+?\n', r'', content_new) # Löschen
    content_new = re.sub(r'\n\([0-9rv]+?\)', r'', content_new) # Löschen
    #content_new = re.sub(r'Anmerkung: .+?\n', r'', content_new) # Löschen
    print(text.group(1),sigle.group(1),initial_page.group(1))
    with open(xml_dir+"/"+text.group(1)+".pta-Ms"+sigle.group(1)+".xml", "w") as f:    
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
        content_new = re.sub(r'<del rend="4">', r'<del rend="unmarked">', content_new)
        content_new = re.sub(r'<del rend="5">', r'<del rend="underline">', content_new)
        #content_new = re.sub(r'5([\w\s]+?)5', r'<add>\1</add>', content_new) # Text über der Zeile; Kurzschreibung # obsolete
        content_new = re.sub(r'5([\w\s]+?)~([1-3]{1})~5', r'<add place="\2">\1</add>', content_new) # Text über der Zeile
        content_new = re.sub(r'<add place="1">', r'<add place="above">', content_new) # auch für Textersetzung
        content_new = re.sub(r'<add place="2">', r'<add place="inline">', content_new)
        content_new = re.sub(r'<add place="3">', r'<add place="margin">', content_new)
        content_new = re.sub(r'6...([0-9a-zA-Z]+?)...6', r'<gap reason="damage" quantity="\1" unit="character"/>', content_new) # Lücke im Text
        content_new = re.sub(r'7...([0-9a-zA-Z]+?)...7', r'<gap reason="illegible" quantity="\1" unit="character"/>', content_new) # Nicht lesbarer Text
        content_new = re.sub(r'8([\w\s@]+?)8', r'<unclear>\1</unclear>', content_new) # unsichere Lesung
        content_new = re.sub(r'9([\w]+?)~([\w]+?)9', r'<choice><expan>\2</expan><abbr type="nomSac"><hi rend="overline">\1</hi></abbr></choice>', content_new) # nomina sacra
        # Zitate
        content_new = re.sub(r'@@', r'<g type="doubled_diple"/>', content_new)
        content_new = re.sub(r'@', r'<g type="diple"/>', content_new)
        content_new = re.sub(r'[–]', r'<g type="paragraphos"/>', content_new)
        # Zahlen
        content_new = re.sub(r'10([\D]{1}?)10', r'<num>\1</num>', content_new)
        # Initialen und Ektheseis
        content_new = re.sub(r'1([\D]{1}?)1', r'<hi rend="initial">\1</hi>', content_new)
        content_new = re.sub(r'2([\D]{1}?)2', r'<hi rend="ekthesis">\1</hi>', content_new)
        # Umbrüche
        #content_new = re.sub(r'\(([\w\d]+?)\)\n', r'', content_new) # Löschen
        content_new = re.sub(r' ///\(([\w\d\.]+?)\) \n', r' <pb n="\1"/> ', content_new)
        content_new = re.sub(r'///\(([\w\d]+?)\)\n', r'<pb n="\1" break="no"/>', content_new) # im Wort
        content_new = re.sub(r' //', r' <cb/> ', content_new)
        content_new = re.sub(r'//', r'<cb break="no"/>', content_new) # im Wort
        content_new = re.sub(r' /[^>\w]{1}', r' <lb/> ', content_new)
        content_new = re.sub(r'/[^>\w]{1}', r'<lb break="no"/>', content_new) # im Wort
        # Titel und Lemma
        title = re.search(r'(?<!\d)0(.+?)(?<!\d)0', content_new, flags=re.DOTALL)
        content_new = re.sub(r'(?<!\d)0(.+?)(?<!\d)0', r'', content_new, flags=re.DOTALL) # Löschen
        ## Ausdruck
       # XML-Grundgerüst
        print('''<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://raw.githubusercontent.com/PatristicTextArchive/Schema/master/tei-pta.rng" schematypens="http://relaxng.org/ns/structure/1.0"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title xml:lang="la">'''+text.group(1)+'''</title>
                <author>XXX</author>
                <respStmt>
                    <resp>transkribiert von</resp>
                    <persName xml:id="'''+editor.group(2)+'''">'''+editor.group(1)+'''</persName>
                </respStmt>
            </titleStmt>
            <editionStmt>
                <p>New transcription.</p>
            </editionStmt>
            <publicationStmt>
                <publisher>Patristic Text Archive</publisher>
                <date>'''+date.group(1)+'''</date>
                <idno type="PTA">'''+text.group(1)+'''</idno>
            </publicationStmt>
            <sourceDesc>
                <msDesc>
                    <msIdentifier xml:id="'''+sigle.group(1)+'''">
                        <settlement>'''+ms.group(1)+'''</settlement>
                        <repository>'''+ms.group(2)+'''</repository>
                        <idno>'''+ms.group(3)+''' '''+ms.group(4)+'''</idno>
                        <altIdentifier type="diktyon">
                            <idno>'''+diktyon.group(1)+'''</idno>
                        </altIdentifier>
                    </msIdentifier>
                </msDesc>'''
          #    <note>'''+comment.group(1)+'''</note>
            '''</sourceDesc>
        </fileDesc>
        <encodingDesc>
            <refsDecl n="CTS">
                <cRefPattern n="chapter" matchPattern="(.+)" replacementPattern="#xpath(/tei:TEI/tei:text/tei:body/tei:div[@type='edition']/tei:div[@n='$1'])"/>
            </refsDecl>
        </encodingDesc>
        <revisionDesc>
            <change who="#'''+editor.group(2)+'''" when="'''+date.group(1)+'''">Transkription des Textes</change>
        </revisionDesc>
    </teiHeader>
    <text xml:lang="grc">
        <body>
            <div type="edition" xml:lang="grc" n="urn:cts:pta:'''+text.group(1)+'''.pta-Ms'''+sigle.group(1)+'''">
            <pb n="'''+initial_page.group(1)+'''"/>
            <head><title>'''+title.group(1)+'''</title></head>
            <div type="textpart" subtype="chapter" n="1">
            <p>'''+content_new+'''</p>
                </div>
                </div>
        </body>
    </text>
</TEI>
    ''', file=f)

