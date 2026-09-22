# Linguagem de escrita de história D²L ✍️

Os arquivos de historia são escritos numa linguagem própria e parseados por um interpretador python linha por linha.

## Sintaxe ❄️
### @FLAGS e @END
O prefixo `@` determina o começo e fim de um bloco, seja de narração ou de dialogo.

Existem ao todo **4 flags** padrão:

    @NARRATOR:   bloco de narrção.
    @DIANA:      bloco de dialogo da Diana.
    @DENA:       bloco de dialogo da Dena.
    @LACEY:      bloco de dialogo da Lacey.
    @OUTRO NOME: bloco de dialogo personalizado.
    @END:        fim do bloco.

Exemplo de uso:
```
    @NARRATOR
    Aqui é uma fala do narrador.
    @END

    @DIANA
    Aqui é uma fala da Diana.
    @END

    @PERSONAGEM ALEATÓRIO
    Aqui é uma fala de outro personagem.
    @END
```

### Parametros personalizados
Use `={}` para indicar parametros de personalização para personagens existentes ou inventados. Os parametros permitidos são:

- `"color"`: Define uma cor personalizada com base em chaves já adicionadas (BLUE, RED, CYAN, etc.). Consulte `utils.py` para saber quais as cores ANSI predefinidas.
- `"speed"`: Define a velocidade de escrita do texto no console.

### Notas importantes
- Caso a flag seja personalizada, a definição de parametros se torna **obrigatória.**
- Caso use parametros em flags já exstentes (`@DIANA`, `@DENA`, etc.), os não definidos terão os valores padrão da flag.
- Não é possível usar o parametro `"color"` em `@NARRATOR`.

Exemplo de uso:
```
@NARRATOR={"speed": 0.08}
Narração mais lenta.
@END

@DIANA={"color": "YELLOW"}
Fala de Diana na cor amarela e na velocidade padrão.
@END

@GABRIEL={"color": "BLUE"}
Personagem criado na cor azul.
@END

```

### 〰️ Citação
Você pode adicionar citações do narrador durante a fala dos personagens com `citation()`. Lembre-se de especificar a citação entre aspas duplas.

```
@DIANA
Nossa... que sorvete gostoso citation("disse Diana, radiante").
@END
```

## FLAGS ESPECIAIS
### ⏰ @WAIT
Determina um tempo de espera blocos.

```
@DIANA
Oii Dena!
@END

@WAIT={"time": 1}

@DENA
... oi.
@END
```

### ✋ @PAUSE
Espera um evento de tecla ENTER do usuário, pausando a execução da história.

```
@NARRATOR
O parque estava especialmente bonito naquela manhã.
Diana, Dena e Lacey andavam sem muito rumo pelo parque, aproveitando o sol matinal.
Diana olhava para as arvores e Lacey andava ao lado dela, e Dena
andava com os olhos no telefone.
@END

@PAUSE

@NARRATOR
...
@END
```
