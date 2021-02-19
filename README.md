# TPA-API

API feita com extração de dados do site [Tudo Para Android](http://www.tudo-para-android.com) usando Python e Flask, ela possibilita obter o link dos consoles disponiveís e os jogos deles, somente isso e nada mais.

# Uso

### Obter os consoles

`GET /api/v1/consoles`

Sem argumentos

### Obter jogos

`GET /api/v1/consoles/{id}`

`{id}` Deve ser substituido pelo número do console na lista(começando de zero);

Argumentos:

    * offset - De onde deve começar(o padrão é 0 que é o inicio);
    * limit - Quantos jogos devem ser devolvidos(o padrão é 200).

### Fazer uma pesquisa por jogos

`GET /api/v1/search/{id}`

`{id}`: Número do console na lista

Argumentos:

    * query - Pesquisa que deve ser feita(suporta regex)
