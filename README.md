# Como Encontrar Seu Dragão

**Subtítulo:** *Eles são lindos, são assustadores, e estão voltando.*

Livro de não-ficção de **Reinaldo Haas** (físico, UFSC) que apresenta a hipótese
**Toró / EOCE** (Extreme Orographic Convective Event) — um fenômeno convectivo extremo
focado pela escarpa, capaz de produzir cabeças d'água, esculpir cânions e, segundo a
hipótese, estar por trás de mitos de serpentes e dragões de água em diversas culturas.

## Estrutura do repositório

- `manuscrito/` — capítulos em Markdown (fonte do livro)
- `montar_livro.py` — script que compila os capítulos em PDF (pandoc + pdflatex + makeindex; A5, 12pt)
- `Como_Encontrar_Seu_Dragao.pdf` — versão compilada mais recente

## Ordem dos capítulos

A ordem oficial está definida na lista `ORDER` dentro de `montar_livro.py`:
Nota de Método → Ato I (caps 1–6) → Ato II (caps 7–10) → Ato III (caps 11, 10b, 12–16)
→ Ato IV (caps 17–21) → Apêndices → Referências.

## Como compilar

Requer `pandoc`, `pdflatex` (TeX Live) e `makeindex`.

```bash
python3 montar_livro.py
```

## Estrutura narrativa (dois movimentos)

- **Movimento A (caps. 1–10):** a palavra "dragão" não aparece.
- **Movimento B (caps. 11+):** o capítulo 11 abre revelando o nome.
