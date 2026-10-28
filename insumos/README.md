# Controle de Insumos — T2 · BRXSP24

App web (mobile/coletor) para registrar entradas, saídas e contagens dos insumos do turno T2.

- **App publicado (link oficial):** https://claude.ai/artifact/ThvGpgJm43bdjrFrZTXEGG
- **Código:** [`app/index.html`](app/index.html), um único arquivo HTML/CSS/JS.
- **Backup dos dados (24/10/2026):** [`backup/insumos.json`](backup/insumos.json) com 25 insumos e saldos, e [`backup/movimentos.json`](backup/movimentos.json) com 3 movimentações.

## Como funciona

- **Registrar:** lista de insumos com os mais retirados nos últimos 7 dias primeiro, mais busca sem acento. Ao tocar num item abre a folha de registro com três opções: Saída, Entrada ou Contagem (ajuste).
- **Saldo:** KPIs do dia (saídas, entradas, contagens), saldo atual de cada insumo e as últimas 30 movimentações do T2.
- Os alertas mostram **zerado** (saldo ≤ 0) e **baixo** (saldo abaixo do `minimo`).

## Dados

Os dados ficam no banco do artifact (`window.claude.use("db")`):

| Coleção | Campos |
|---|---|
| `insumos/{id}` | `nome`, `saldo`, `minimo`, `prioridade?`, `unidade?` (padrão "Uni"), `ativo` |
| `movimentos/{auto}` | `insumoId`, `tipo` (`saida`/`entrada`/`ajuste`), `qtd`, `contado?`, `turno`, `quem`, `ts` |

> O `index.html` só funciona com dados dentro do Claude (artifact). Se abrir o arquivo localmente, ele mostra "Offline".

## AppSheet + Google Sheets (versão para o HF)

O app do Claude roda dentro do domínio claude.ai e o HF não consegue bipar nele. A versão para o turno é no **AppSheet**, com os dados na planilha **Controle de Insumos T2** do Google Drive.

- Passo a passo para montar o app: [`appsheet/PASSO-A-PASSO.md`](appsheet/PASSO-A-PASSO.md)
- Cópia da planilha: [`appsheet/Controle_de_Insumos_T2.xlsx`](appsheet/Controle_de_Insumos_T2.xlsx)

## Etiquetas QR

- PDF pronto para imprimir: [`etiquetas/etiquetas-qr.pdf`](etiquetas/etiquetas-qr.pdf), em A4 com 15 por folha.
- O QR traz só o **ID** do insumo (ex.: `fita-adesiva`), que é a chave da aba Insumos e é o que o AppSheet reconhece.
- Ao cadastrar um insumo novo, gere o PDF de novo: `python3 tools/gerar_etiquetas.py backup/insumos.json etiquetas/etiquetas-qr.pdf`
