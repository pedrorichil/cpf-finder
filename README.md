# PESQUISADOR DE CPF DE FORÇA BRUTA

O CPF (Cadastro de Pessoas Físicas) é um documento de identificação utilizado em
Brasil. É um número único e individual atribuído a cada brasileiro
cidadão. É utilizado para identificação em diversas situações, como
abertura de contas bancárias, realização de compras, contratação de serviços, entre outros.
Para obter o CPF é necessário se cadastrar na Receita Federal.


Este script utiliza um dos principais serviços da rede federal brasileira
governo para descobrir informações baseadas no nome do cidadão registrado.
Baseia-se na vulnerabilidade do Portal da Transparência, que
expõe parte do CPF do cidadão e censura apenas os 3 primeiros dígitos e o
dígitos de verificação. Como o CPF segue um padrão restrito de dígitos, por
expondo 6 de um total de 11 dígitos, o Portal da Transparência reduz o
número de combinações para 100.000. Porém, como o CPF utiliza os últimos 2
dígitos para verificação dos 9 anteriores, é possível reduzir o espaço
de possibilidades para apenas 1.000 combinações, o que é bastante viável para um
ataque de força bruta.

## Significado dos Dígitos do CPF

O CPF é composto por 11 dígitos e tem um significado específico para cada um deles.
eles. Uma representação comum do CPF consiste em agrupar os primeiros nove
dígitos em três grupos de três dígitos separados por um ponto, seguido por um
hífen e os dois últimos dígitos. Assim, o número do CPF ABCDEFGHIJK fica formatado
como ABC.DEF.GHI-JK. Neste caso, são utilizados os dígitos representados por J e K
como dígitos de verificação.


Cada dígito do CPF tem um significado específico. Os primeiros oito dígitos, ABCDEFGH,
formar o número base definido pela Receita Federal no momento da
cadastro. O nono dígito, I, define a região onde o CPF foi emitido.
O décimo dígito é o primeiro dígito de verificação. O décimo primeiro dígito é o
segundo dígito de verificação.


### Como funcionam os dígitos de verificação

O primeiro dígito de verificação, J, é o dígito de verificação dos primeiros nove
dígitos. O segundo dígito de verificação, K, é o dígito de verificação para o
nove dígitos antes dele. Os primeiros nove dígitos são multiplicados sequencialmente por
a sequência {10, 9, 8, 7, 6, 5, 4, 3, 2} (o primeiro por 10, o segundo por 9,
e assim por diante). Então, o resto R da divisão da soma dos
os resultados da multiplicação por 11 são calculados. Se o resto for 0 ou 1, o
o primeiro dígito é zero (ou seja, J=0); caso contrário, J=11 - R.


O segundo Dígito de Verificação, K, é calculado pela mesma regra, onde o
números a serem multiplicados pela sequência {10, 9, 8, 7, 6, 5, 4, 3, 2} são
contado a partir do segundo dígito, sendo J agora o último dígito. Se S
é o resto da divisão por 11 da soma das multiplicações,
então K será 0 se S for 0 ou 1. Caso contrário, K=11-S.


## Como funciona o script

Este script possui 2 parâmetros de linha de comando: `--name` (obrigatório) e
`--palavra-chave`. O parâmetro `--name` deve conter o nome completo do
cidadão cujo CPF você deseja descobrir. Se este nome completo for exclusivo no
banco de dados, o script fará o download e a análise do CPF parcial
disponibilizado pelo Portal da Transparência. Com base nesse CPF parcial, o roteiro
gera todas as combinações possíveis, encontra as válidas de acordo com o CPF
algoritmo de validação descrito acima e, em seguida, tenta, por meio de força bruta,
fazer uma série de solicitações com base nesse CPF gerado e validado. Se
o CPF existe no banco de dados, avisa o script. O programa para quando
o nome completo encontrado corresponde ao nome passado através do parâmetro `--name`.


Por exemplo, suponha que você queira encontrar o CPF do presidente do Brasil, Sr.
Luiz Inácio Lula da Silva:

```bash
python script.py --name "LUIZ INACIO LULA DA SILVA"
```

Após realizar diversas tentativas, o script reportará todos os CPFs encontrados no Portal
da Transparência e então para quando o CPF descoberto corresponderá a
o mesmo nome passado por `--name`.

Parâmetro `--keyword`: quando for informado o nome completo do cidadão cujo CPF você deseja
para descobrir é único no banco de dados, o comando acima é suficiente.
Porém, em alguns casos, podem existir nomes homônimos ou muito semelhantes. Em
nesses casos, é possível repassar o padrão do CPF parcial fornecido
pelo próprio Portal da Transparência (ex.: `***.680.938-**`). Nesse caso,
você deve fornecer o nome completo (ou seja, parâmetro --name), bem como o
Parâmetro `--keyword`. Assim, o parâmetro --keyword será usado como o
critério de pesquisa e o parâmetro `--name como critério de parada.

Por exemplo, suponha que você queira descobrir o CPF completo do ex-
presidente do Brasil, Sra. Dilma Vana Rousseff, sabendo que parte de seu CPF está
`***.267.246-**`, conforme fornecido pelo
[Portal da Transparência](https://portaldatransparencia.gov.br/pessoa-fisica/busca/lista?):

```bash
python script.py --name "DILMA VANA ROUSSEFF" --keyword "***.267.246-**"
```

Exemplo de execução deste script disponível no vídeo: [https://youtu.be/c13g8o0wMJs](https://youtu.be/c13g8o0wMJs).
