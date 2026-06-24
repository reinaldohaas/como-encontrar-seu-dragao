# Como Encontrar Seu Dragão

**Subtítulo:** *Eles são lindos, são assustadores, e estão voltando.*

Livro de não-ficção de **Reinaldo Haas** (físico, UFSC) sobre a hipótese **Toró / EOCE**
(Extreme Orographic Convective Event). Propósito do livro: validar o **InfraLABMIT** e a
missão de **encontrar e mitigar** o EOCE, dar contexto ao fenômeno, e mobilizar apoio para
uma ONG.

## Estrutura
- `manuscrito/` — capítulos em Markdown (fonte do livro)
- `montar_livro.py` — compila os capítulos em PDF (pandoc + pdflatex + makeindex; A5, 12pt)
- `Como_Encontrar_Seu_Dragao.pdf` — PDF compilado
- `documentos_trabalho/` — documentos de estado do projeto (planejamento e pesquisa):
  - `PLANO_REESTRUTURACAO.md` — nova estrutura, cortes, propósito, conteúdo novo a integrar
  - `REFERENCIAS_ASSINATURAS.md` — as 7 assinaturas do EOCE, critério de poda, janela
    estreita de precondições, referências de infrasom operacional e stormquakes
  - `RELATOS_ASSINATURAS.md` — depoimentos reais coletados (som, tremor, iridiscência) +
    fontes acadêmicas (Kobiyama/GPDEN-UFRGS) + lista de buscas pendentes
  - `ACOES_CRITICA_DEEPSEEK.md` — respostas à crítica editorial
  - `Como_Encontrar_Seu_Dragao_EDICAO_REVISAO.docx` — livro com notas de revisão por capítulo

## Como compilar
Requer `pandoc`, `pdflatex` (TeX Live) e `makeindex`:
```bash
python3 montar_livro.py
```

## Pendências (dependem do autor)
- Como refazer a revelação do dragão (cap.11).
- Material dos eventos do RS; cidade exata do Taquari (família Lohmann).
- Referência exata da publicação CEMADEN (+13 mil movimentos de massa no RS).
- Trechos de "Harmonia e Tempestades"; nome do observador da Epagri a homenagear.
