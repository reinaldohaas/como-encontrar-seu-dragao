#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta o livro completo (22 caps + apêndices) em LaTeX e compila o PDF."""
import subprocess, os, re, sys

BASE = "/home/claude/toro_dragao"
MAN = os.path.join(BASE, "livro/manuscrito")
OUT = os.path.join(BASE, "livro/latex")
os.makedirs(OUT, exist_ok=True)

# ordem dos capítulos e a que Ato pertencem
ORDER = [
    ("NOTA_METODO", None),
    ("PARTE", "Ato I — A Semente"),
    ("cap01", None), ("cap02", None), ("cap03", None),
    ("cap04", None), ("cap05", None), ("cap06", None),
    ("PARTE", "Ato II — O Despertar"),
    ("cap07", None), ("cap08", None), ("cap09", None),
    ("cap10", None),
    ("PARTE", "Ato III — A Caçada"),
    ("cap11", None), ("cap10b", None), ("cap12", None), ("cap13", None),
    ("cap14", None), ("cap15", None), ("cap16", None),
    ("PARTE", "Ato IV — A Perda e o Retorno"),
    ("cap17", None), ("cap18", None), ("cap19", None),
    ("cap20", None), ("cap21", None),
    ("APENDICES", None),
]

def find(prefix):
    for fn in sorted(os.listdir(MAN)):
        if fn.startswith(prefix + "_") or fn == prefix + ".md":
            return os.path.join(MAN, fn)
    return None

def md_to_tex(path, is_appendix=False):
    """Converte um .md para corpo LaTeX via pandoc, removendo o front-matter YAML.
    Remove a linha '# Capítulo N' / '# Epílogo' redundante e promove o subtítulo
    '## Título' a capítulo, para o LaTeX numerar sozinho (sem 'Chapter 1. Capítulo 1')."""
    txt = open(path, encoding="utf-8").read()
    # remover front-matter YAML (entre os dois primeiros ---)
    if txt.startswith("---"):
        parts = txt.split("---", 2)
        if len(parts) >= 3:
            txt = parts[2]
    lines = txt.split("\n")
    out_lines = []
    is_epilogue = False
    if is_appendix:
        # apêndices: descartar o primeiro "# Apêndices" (vira \ato);
        # cada "# Título" seguinte permanece como H1 (\chapter -> "Apêndice A...")
        dropped_intro = False
        for ln in lines:
            s = ln.strip()
            if not dropped_intro and s.lower().startswith("# apêndice"):
                dropped_intro = True
                continue
            out_lines.append(ln)
        txt = "\n".join(out_lines)
        p = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex",
                            "--top-level-division=chapter"],
                           input=txt, capture_output=True, text=True)
        if p.returncode != 0:
            print("pandoc erro:", p.stderr[:500]); sys.exit(1)
        out = p.stdout
        repl = {"龍": "lóng", "龙": "lóng", "黎": "", "雷": "", "珠": ""}
        for k, v in repl.items():
            out = out.replace(k, v)
        out = re.sub(r"[\u3000-\u9fff\uf900-\ufaff]", "", out)
        return out
    removed_h1 = False
    for ln in lines:
        s = ln.strip()
        # descartar o H1 "# Capítulo N" ou "# Epílogo"
        if not removed_h1 and s.startswith("# "):
            if s.lower().startswith("# epílogo") or s.lower().startswith("# epilogo"):
                is_epilogue = True
            removed_h1 = True
            continue
        # promover o primeiro "## Título" a "# Título" (vira \chapter)
        if removed_h1 and s.startswith("## "):
            out_lines.append("# " + s[3:])
            removed_h1 = "done"  # marca que já promoveu
            continue
        out_lines.append(ln)
    txt = "\n".join(out_lines)
    p = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex",
                        "--top-level-division=chapter"],
                       input=txt, capture_output=True, text=True)
    if p.returncode != 0:
        print("pandoc erro:", p.stderr[:500]); sys.exit(1)
    out = p.stdout
    # Epílogo: transformar o \chapter em \chapter* (sem número) + entrada no TOC
    if is_epilogue:
        out = re.sub(r"\\chapter\{([^}]*)\}",
                     r"\\chapter*{\1}\n\\addcontentsline{toc}{chapter}{\1}",
                     out, count=1)
    # pdflatex não suporta CJK/Unicode alto; substituir caracteres problemáticos
    repl = {"龍": "lóng", "龙": "lóng", "黎": "", "雷": "", "珠": ""}
    for k, v in repl.items():
        out = out.replace(k, v)
    # remover quaisquer outros caracteres CJK remanescentes (faixa Han)
    out = re.sub(r"[\u3000-\u9fff\uf900-\ufaff]", "", out)
    return out

PREAMBLE = r"""\documentclass[12pt,a5paper,openany]{book}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\renewcommand{\chaptername}{Capítulo}
\renewcommand{\contentsname}{Sumário}
\renewcommand{\appendixname}{Apêndice}
\usepackage[a5paper,inner=1.9cm,outer=1.5cm,top=1.9cm,bottom=2.0cm]{geometry}
\usepackage{setspace}\onehalfspacing
\usepackage{titlesec}
\usepackage{titletoc}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage{tikz}
\usepackage{makeidx}
\makeindex
\definecolor{tinta}{RGB}{30,30,38}
\definecolor{cinzaescuro}{RGB}{90,90,100}
\definecolor{cinzamedio}{RGB}{120,120,130}
% paleta da capa
\definecolor{ceunoite}{RGB}{18,22,40}
\definecolor{ceualto}{RGB}{40,52,92}
\definecolor{irisA}{RGB}{120,170,200}
\definecolor{irisB}{RGB}{180,150,200}
\definecolor{irisC}{RGB}{210,170,150}
\definecolor{aguaclara}{RGB}{170,205,220}
\definecolor{montanha}{RGB}{12,16,28}
\definecolor{douro}{RGB}{206,178,120}
\definecolor{cinzaclaro}{RGB}{220,225,235}
% --- suporte a Unicode comum no pdflatex ---
\DeclareUnicodeCharacter{03BC}{$\mu$}
\DeclareUnicodeCharacter{03C1}{$\rho$}
\DeclareUnicodeCharacter{00BD}{$\frac{1}{2}$}
\DeclareUnicodeCharacter{2248}{$\approx$}
\DeclareUnicodeCharacter{2192}{$\rightarrow$}
\DeclareUnicodeCharacter{2194}{$\leftrightarrow$}
\DeclareUnicodeCharacter{00D7}{$\times$}
\DeclareUnicodeCharacter{2261}{$\equiv$}
\DeclareUnicodeCharacter{2013}{--}
\DeclareUnicodeCharacter{2014}{---}
\DeclareUnicodeCharacter{2026}{\ldots}
\DeclareUnicodeCharacter{02C8}{'}
\DeclareUnicodeCharacter{0303}{\textasciitilde}
\DeclareUnicodeCharacter{028B}{v}
\DeclareUnicodeCharacter{0294}{'}
\DeclareUnicodeCharacter{014B}{ng}
\DeclareUnicodeCharacter{0144}{\'n}
\DeclareUnicodeCharacter{02D0}{:}
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[C]{\thepage}
% --- título de capítulo ---
\titleformat{\chapter}[display]
  {\normalfont\bfseries\color{tinta}}
  {\filright\large\color{cinzaescuro}\chaptertitlename\ \thechapter}
  {0.4em}{\LARGE\filright}
\titlespacing*{\chapter}{0pt}{6pt}{20pt}
% --- comando \ato : cabeçalho de ato SEM quebra de página, SEM "Parte" ---
\newcommand{\ato}[1]{%
  \par\vspace{0.5\baselineskip}%
  {\centering\color{cinzamedio}\rule{0.30\textwidth}{0.4pt}\par}%
  \vspace{0.7\baselineskip}%
  {\centering\large\scshape\color{tinta}#1\par}%
  \vspace{0.4\baselineskip}%
  {\centering\color{cinzamedio}\rule{0.30\textwidth}{0.4pt}\par}%
  \vspace{1.0\baselineskip}%
  \addcontentsline{toc}{section}{\textsc{#1}}%
}
% --- \chapternobreak : um \chapter que NÃO quebra a página (p/ 1º cap do ato) ---
\newcommand{\chapternobreak}[1]{%
  \begingroup
  \let\clearpage\relax
  \let\cleardoublepage\relax
  \chapter{#1}%
  \endgroup
}
% --- sumário mais legível ---
\setcounter{tocdepth}{1}
\titlecontents{chapter}[1.5em]{\vspace{2pt}\bfseries}
  {\contentslabel{1.5em}}{\hspace*{-1.5em}}
  {\titlerule*[0.6pc]{.}\contentspage}
\titlecontents{section}[0em]{\vspace{6pt}\scshape\color{tinta}}
  {}{}{\hfill}
% pandoc helpers
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\usepackage{hyperref}\hypersetup{hidelinks}
\begin{document}
% capítulos abrem na próxima página (par ou ímpar): sem folhas em branco de paridade
\let\cleardoublepage\clearpage
% ============ CAPA ============
\thispagestyle{empty}
\begin{titlepage}
\noindent\begin{tikzpicture}[remember picture,overlay]
  \shade[top color=ceunoite, bottom color=ceualto]
    (current page.south west) rectangle (current page.north east);
  \begin{scope}
    \clip (current page.south west) rectangle (current page.north east);
    \foreach \r/\c/\o in {3.2/irisA/30, 2.5/irisB/35, 1.8/irisC/40, 1.1/aguaclara/55}{
      \fill[\c, opacity=\o/100] ([yshift=3.6cm]current page.center) circle (\r cm);
    }
    \fill[aguaclara, opacity=0.85]
      ([xshift=-0.45cm,yshift=3.4cm]current page.center)
      .. controls ([xshift=1.1cm,yshift=1.6cm]current page.center)
         and ([xshift=-1.3cm,yshift=0.2cm]current page.center)
      .. ([xshift=0.2cm,yshift=-1.8cm]current page.center)
      .. controls ([xshift=0.9cm,yshift=-3.1cm]current page.center)
         and ([xshift=-0.5cm,yshift=-4.0cm]current page.center)
      .. ([xshift=0.0cm,yshift=-5.6cm]current page.center)
      -- ([xshift=0.6cm,yshift=-5.6cm]current page.center)
      .. controls ([xshift=0.1cm,yshift=-3.7cm]current page.center)
         and ([xshift=1.6cm,yshift=-2.9cm]current page.center)
      .. ([xshift=0.9cm,yshift=-1.7cm]current page.center)
      .. controls ([xshift=-0.5cm,yshift=0.3cm]current page.center)
         and ([xshift=1.8cm,yshift=1.7cm]current page.center)
      .. ([xshift=0.25cm,yshift=3.4cm]current page.center)
      -- cycle;
    \fill[montanha]
      ([xshift=0cm]current page.south west) -- ([yshift=3.0cm]current page.south west)
      .. controls ([xshift=2.5cm,yshift=1.8cm]current page.south west)
         and ([xshift=3.5cm,yshift=1.0cm]current page.south west)
      .. ([xshift=4.6cm,yshift=0cm]current page.south west) -- cycle;
    \fill[montanha]
      ([xshift=0cm]current page.south east) -- ([yshift=3.4cm]current page.south east)
      .. controls ([xshift=-2.2cm,yshift=2.0cm]current page.south east)
         and ([xshift=-3.6cm,yshift=0.9cm]current page.south east)
      .. ([xshift=-4.8cm,yshift=0cm]current page.south east) -- cycle;
  \end{scope}
  \node[align=center, text=cinzaclaro] at ([yshift=-1.5cm]current page.north) {
    {\fontsize{29}{33}\selectfont\bfseries Como Encontrar}\\[2pt]
    {\fontsize{29}{33}\selectfont\bfseries Seu Dragão}};
  \draw[douro, line width=0.8pt]
    ([xshift=-2.0cm,yshift=-2.95cm]current page.north) --
    ([xshift=2.0cm,yshift=-2.95cm]current page.north);
  \node[align=center, text=douro, font=\itshape] at ([yshift=-3.6cm]current page.north) {
    Eles são lindos, são assustadores,\\ e estão voltando};
  \node[align=center, text=cinzaclaro] at ([yshift=1.5cm]current page.south) {
    {\large Reinaldo Haas}};
\end{tikzpicture}
\end{titlepage}
% ============ CONTRACAPA / ORELHA ============
\thispagestyle{empty}
\begin{titlepage}
\noindent\begin{tikzpicture}[remember picture,overlay]
  \shade[top color=ceunoite, bottom color=ceualto]
    (current page.south west) rectangle (current page.north east);
  \node[align=center, text=douro, font=\large\itshape, text width=10cm]
    at ([yshift=-2.2cm]current page.north)
    {Você acredita que dragões cospem fogo?};
  \node[align=left, text=cinzaclaro, font=\normalsize, text width=10.2cm]
    at ([yshift=0.2cm]current page.center)
    {Pois você foi enganado.\\[7pt]
     Durante séculos, contaram a você a história errada: um monstro de fogo, asas de
     morcego, ouro no covil. Esqueça tudo isso.\\[7pt]
     Os dragões existiram --- e ainda existem. Mas não cospem fogo. Eles
     \textit{despejam água}. São colunas vivas de gelo e tempestade que descem do céu,
     escavam vales inteiros num só golpe, fazem a terra tremer e se anunciam em cores no
     ar. Quase toda cultura humana os viu. Quase toda cultura humana lhes deu um nome.\\[7pt]
     Este livro é a história de como um físico, seguindo a palavra de seu pai diante de um
     riacho transbordado, reencontrou essa criatura --- na física das nuvens, na memória
     dos mitos, na cicatriz que ela deixa na pedra.\\[7pt]
     Eles são lindos. Fizeram um trabalho hercúleo: esculpiram a paisagem do planeta. E
     por isso mesmo são assustadores.\\[7pt]
     E, agora que o céu volta a ficar limpo, eles estão voltando.};
  \node[align=center, text=douro, font=\small]
    at ([yshift=1.4cm]current page.south)
    {Reinaldo Haas $\cdot$ Universidade Federal de Santa Catarina};
\end{tikzpicture}
\end{titlepage}
\frontmatter
\begin{titlepage}\centering\vspace*{4cm}
{\Huge\bfseries\color{tinta} Como Encontrar Seu Dragão}\\[0.8cm]
{\large\itshape Eles são lindos, são assustadores, e estão voltando}\\[3cm]
{\large Reinaldo Haas}\\[0.5cm]
{\small Universidade Federal de Santa Catarina}\par
\vfill {\small Manuscrito --- versão de trabalho}\par\end{titlepage}
\tableofcontents
\mainmatter
"""

def _ato_label(label):
    """Mantém o rótulo do ato como está (ex.: 'Ato I — A Semente')."""
    return label

# termos-chave para o índice remissivo (regex insensível -> entrada canônica)
INDEX_TERMS = [
    (r"\btoró\b", "toró"),
    (r"\btromba d'água\b", "tromba d'água"),
    (r"\btrombudo\b", "trombudo"),
    (r"\bcabeça d'água\b", "cabeça d'água"),
    (r"\bdragão\b", "dragão"),
    (r"\bdragões\b", "dragão"),
    (r"\bPasteur\b", "Pasteur, Louis"),
    (r"\bWegener\b", "Wegener, Alfred"),
    (r"\bSagan\b", "Sagan, Carl"),
    (r"\bHallett-Mossop\b", "Hallett-Mossop, processo"),
    (r"\bPhillips\b", "Phillips, multiplicação de gelo"),
    (r"\bJoukowsky\b", "Joukowsky (golpe de aríete)"),
    (r"\bgolpe de aríete\b", "golpe de aríete"),
    (r"\bShields\b", "Shields, critério de"),
    (r"\bsinteriza", "sinterização"),
    (r"\biodo\b", "iodo marinho"),
    (r"\bchumbo\b", "chumbo (aerossol)"),
    (r"\bágua super-resfriada\b", "água super-resfriada"),
    (r"\bValada São Paulo\b", "Valada São Paulo"),
    (r"\bItajaí-Mirim\b", "Itajaí-Mirim, rio"),
    (r"\bVidal Ramos\b", "Vidal Ramos"),
    (r"\bBrusque\b", "Brusque"),
    (r"\bTimbé do Sul\b", "Timbé do Sul"),
    (r"\bJacinto Machado\b", "Jacinto Machado"),
    (r"\bSerra Geral\b", "Serra Geral"),
    (r"\bXokleng\b", "Xokleng (Laklãnõ)"),
    (r"\bEpagri\b", "Epagri"),
    (r"\bTDAH\b", "TDAH"),
    (r"\bAumond\b", "Aumond, Juarez"),
    (r"\bHodecker\b", "Hodecker, Alessandra"),
    (r"\bimbuia\b", "imbuia"),
    (r"\bdam-break\b", "dam-break (rompimento)"),
    (r"\blóng\b", "lóng (dragão chinês)"),
    (r"\bhoro\b", "horo (māori)"),
    (r"\bJuan Flores\b", "Flores, Juan"),
    (r"\bDr\. Juan Flores\b", "Flores, Juan"),
    (r"\bLucas\b", "Lucas (filho do autor)"),
    (r"\batividade elétrica\b", "atividade elétrica"),
    (r"\brelâmpago", "relâmpago"),
    (r"\bAmaru\b", "Amaru (andino)"),
    (r"\bOilliph", "Oilliphéist (irlandês)"),
    (r"\bShannon\b", "Shannon, rio"),
    (r"\bSerpente Arco-[ÍI]ris\b", "Serpente Arco-Íris"),
    (r"\bbow-echo\b", "bow-echo"),
    (r"\binselberg\b", "inselberg"),
    (r"\bGrande Inconformidade\b", "Grande Inconformidade"),
    (r"\bCambriana?\b", "Explosão Cambriana"),
    (r"\biridescen", "iridescência"),
    (r"\bcorrida de detritos\b", "corrida de detritos"),
    (r"\bHarmonia e Tempestades\b", "Harmonia e Tempestades"),
]

def _add_index_marks(tex):
    """Insere \\index{termo} na primeira ocorrência de cada termo-chave, mas só em
    linhas de texto corrido — nunca dentro de \\hypertarget, \\chapter, \\section,
    \\label, \\index ou linhas de comando (que começam com barra invertida)."""
    lines = tex.split("\n")
    done = set()
    skip_prefixes = ("\\hypertarget", "\\chapter", "\\section", "\\subsection",
                     "\\label", "\\part", "\\ato", "\\begin", "\\end", "%")
    for li, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(skip_prefixes):
            continue
        for pat, entry in INDEX_TERMS:
            if entry in done:
                continue
            m = re.search(pat, line, flags=re.IGNORECASE)
            if m:
                pos = m.end()
                line = line[:pos] + ("\\index{%s}" % entry) + line[pos:]
                done.add(entry)
        lines[li] = line
    return "\n".join(lines)

def _suppress_first_clearpage(tex):
    """Troca o primeiro \\chapter{...} por \\chapternobreak{...} para que o
    capítulo não quebre a página e fique junto do cabeçalho do Ato."""
    return re.sub(r"\\chapter\{", r"\\chapternobreak{", tex, count=1)

body = [PREAMBLE]
pending_ato = False
for key, label in ORDER:
    if key == "NOTA_METODO":
        f = find("nota_metodo")
        if f:
            chap = md_to_tex(f)
            # transformar o \chapter em \chapter* (sem número) e registrar no sumário
            chap = chap.replace("\\chapternobreak{", "\\chapter*{", 1)
            chap = re.sub(r"\\chapter\{", r"\\chapter*{", chap, count=1)
            body.append("\n" + chap + "\n")
        continue
    if key == "PARTE":
        # marca: o próximo capítulo deve vir na MESMA página que este Ato
        body.append("\n\\ato{%s}\n" % _ato_label(label))
        pending_ato = True
    elif key == "APENDICES":
        body.append("\n\\appendix\n\\ato{Apêndices}\n")
        pending_ato = True
        f = find("apendices")
        if f:
            tex_ap = md_to_tex(f, is_appendix=True)
            if pending_ato:
                tex_ap = _suppress_first_clearpage(tex_ap)
                pending_ato = False
            body.append(tex_ap)
    else:
        f = find(key)
        if not f:
            print("FALTA:", key); continue
        chap = md_to_tex(f)
        chap = _add_index_marks(chap)
        if pending_ato:
            chap = _suppress_first_clearpage(chap)
            pending_ato = False
        body.append("\n" + chap + "\n")
# ===== BACKMATTER: bibliografia + índice remissivo =====
body.append("\n\\backmatter\n")
ref = find("referencias")
if ref:
    body.append("\n\\ato{Referências}\n" + _suppress_first_clearpage(md_to_tex(ref)) + "\n")
body.append("\n\\clearpage\n\\renewcommand{\\indexname}{Índice Remissivo}\n\\printindex\n")
body.append("\n\\end{document}\n")

tex = "\n".join(body)
texpath = os.path.join(OUT, "livro_completo.tex")
open(texpath, "w", encoding="utf-8").write(tex)
print("livro_completo.tex montado:", len(tex), "chars")

# compilar 2x (TOC)
os.chdir(OUT)
def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace")
# passada 1
r = _run(["pdflatex", "-interaction=nonstopmode", "livro_completo.tex"])
print("pdflatex passada 1: rc=%d" % r.returncode)
# gerar o índice remissivo
ri = _run(["makeindex", "livro_completo.idx"])
print("makeindex: rc=%d" % ri.returncode)
# passadas 2 e 3 (TOC + índice + referências cruzadas)
for i in range(2, 4):
    r = _run(["pdflatex", "-interaction=nonstopmode", "livro_completo.tex"])
    print("pdflatex passada %d: rc=%d" % (i, r.returncode))
if not os.path.exists(os.path.join(OUT, "livro_completo.pdf")):
    print(r.stdout[-1500:])
print("PDF gerado:", os.path.exists(os.path.join(OUT, "livro_completo.pdf")))
