# App de Insumos no AppSheet: passo a passo

Planilha (Google Drive): **Controle de Insumos T2**
https://docs.google.com/spreadsheets/d/1cLPLCJeZSLlliCreiwb4M80pJ-ftqkdn4h8QNyN0PkI/edit

## Como a planilha funciona

- **Insumos**: um insumo por linha. As colunas `Ult_contagem`, `Saldo` e `Status` são fórmulas: **não digite nelas**.
- **Movimentos**: cada registro do app vira uma linha nova (Saída, Entrada ou Contagem).
- **Saldo** = última Contagem + Entradas − Saídas registradas depois dela.
- Os saldos de hoje entraram como uma Contagem de "Saldo inicial (migração)" em 28/10/2026 00:00. As 3 saídas antigas ficaram só como histórico.

## 1. Criar o app (5 min)

1. Abra a planilha e vá em **Extensões → AppSheet → Criar um app**.
2. O AppSheet abre o editor e importa a aba **Insumos**.
3. Vá em **Data → + (Add Table)**, escolha a mesma planilha e adicione a aba **Movimentos**.

## 2. Ajustar as colunas

**Data → Insumos → Columns**

| Coluna | Type | Ajustes |
|---|---|---|
| ID | Text | Key ✔, **Scannable ✔** |
| Nome | Name | Label ✔ |
| Ult_contagem, Saldo, Status | (automático) | Editable ✘ (são fórmulas da planilha) |
| Ativo | Yes/No | |

**Data → Movimentos → Columns**

| Coluna | Type | Ajustes |
|---|---|---|
| ID | Text | Key ✔, Initial value: `UNIQUEID()`, Show ✘ |
| Data_hora | DateTime | Initial value: `NOW()`, Editable ✘ |
| Insumo | **Ref** → Insumos | **Scannable ✔**, Required ✔ |
| Tipo | Enum | Valores: `Saída`, `Entrada`, `Contagem`; Initial value: `"Saída"`; Input mode: Buttons |
| Quantidade | Number | Required ✔; Valid if: `[_THIS] >= 0` |
| Turno | Enum | Valores: `T1`, `T2`, `T3`; Initial value: `"T2"` |
| Quem | Text | Initial value: `USEREMAIL()` (ou deixe o operador digitar o nome) |

Para impedir saída maior que o saldo, coloque em **Quantidade → Valid if**:

```
OR([Tipo] <> "Saída", [_THIS] <= [Insumo].[Saldo])
```

## 3. Telas (UX → Views)

- **Registrar**: Table = Movimentos, View type = **Form**. É a tela principal do HF.
- **Saldo**: Table = Insumos, View type = Table, colunas Nome, Saldo e Status.
- **Histórico**: Table = Movimentos, View type = Table, ordenado por Data_hora (decrescente).

Em **UX → Format Rules** dá para pintar Status = "Zerado" de vermelho e "Baixo" de amarelo.

## 4. Bipar com o HF

Os QR codes do PDF `etiquetas/etiquetas-qr.pdf` trazem só o **ID** do insumo, por exemplo `fita-adesiva`.

- **HF com leitor físico (Zebra/Honeywell)**: abra o app **AppSheet** (Play Store) ou o link do app no Chrome do HF. Na tela Registrar, toque no campo **Insumo** e aperte o gatilho. O leitor digita o ID e o AppSheet seleciona o insumo.
  - O leitor precisa estar no modo "teclado" (Keystroke / Keyboard wedge). É o padrão do DataWedge (Zebra) e do Scanner Settings (Honeywell).
- **Celular**: o ícone de código de barras ao lado do campo Insumo abre a câmera.

## 5. Publicar para o turno

1. **Share** (canto de cima): adicione o e-mail de cada operador, ou libere para "qualquer pessoa com conta Google" se o plano permitir.
2. No HF: instale o **AppSheet**, entre com a conta do operador e abra o app "Controle de Insumos T2".
3. O app funciona offline e sincroniza quando volta o Wi-Fi.

> Plano grátis do AppSheet: até 10 usuários em modo protótipo, suficiente para testar. Para o turno inteiro de forma oficial, veja com a empresa se ela tem Google Workspace com AppSheet incluído.

## Insumo novo

Adicione uma linha na aba Insumos com **ID**, **Nome**, **Unidade**, **Minimo** e **Ativo = TRUE**. As fórmulas das colunas G a I são copiadas da linha de cima. Depois registre uma **Contagem** dele no app e gere a etiqueta:

```
python3 tools/gerar_etiquetas.py backup/insumos.json etiquetas/etiquetas-qr.pdf
```

(ou peça para o Claude gerar a etiqueta nova)
