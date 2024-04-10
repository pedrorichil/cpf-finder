# BRUTE FORCE CPF FINDER

The CPF (Cadastro de Pessoas Físicas) is an identification document used in
Brazil. It is a unique and individual number assigned to each Brazilian
citizen. It is used for identification in various situations, such as
opening bank accounts, making purchases, contracting services, among others.
To obtain a CPF, it is necessary to register with the Federal Revenue Service.


This script uses one of the main services of the Brazilian federal
government to discover information based on the registered citizen's name.
It relies on the vulnerability of the Portal da Transparência, which
exposes part of the citizen's CPF and censors only the first 3 digits and the
verification digits. Since the CPF follows a restricted pattern of digits, by
exposing 6 out of a total of 11 digits, the Transparency Portal reduces the
number of combinations to 100,000. However, since the CPF uses the last 2
digits for verification of the previous 9, it is possible to reduce the space
of possibilities to only 1,000 combinations, which is quite feasible for a
brute force attack.

## Meaning of the CPF Digits

The CPF consists of 11 digits and has a specific meaning for each one of
them. A common representation of the CPF consists of grouping the first nine
digits into three groups of three digits separated by a period, followed by a
hyphen and the last two digits. Thus, the CPF number ABCDEFGHIJK is formatted
as ABC.DEF.GHI-JK. In this case, the digits represented by J and K are used
as verification digits.


Each digit of the CPF has a specific meaning. The first eight digits, ABCDEFGH,
form the base number defined by the Federal Revenue Service at the time of
registration. The ninth digit, I, defines the region where the CPF was issued. 
The tenth digit is the first verification digit. The eleventh digit is the
second verification digit. 


### How Verification Digits Work

The first verification digit, J, is the verification digit for the first nine
digits. The second verification digit, K, is the verification digit for the
nine digits before it. The first nine digits are sequentially multiplied by
the sequence {10, 9, 8, 7, 6, 5, 4, 3, 2} (the first by 10, the second by 9,
and so on). Then, the remainder R of the division of the sum of the
multiplication results by 11 is calculated. If the remainder is 0 or 1, the
first digit is zero (i.e., J=0); otherwise, J=11 - R.


The second Verification Digit, K, is calculated by the same rule, where the
numbers to be multiplied by the sequence {10, 9, 8, 7, 6, 5, 4, 3, 2} are
counted starting from the second digit, with J now being the last digit. If S
is the remainder of the division by 11 of the sum of the multiplications,
then K will be 0 if S is 0 or 1. Otherwise, K=11-S.


## How the Script Works

This script has 2 command-line parameters: `--name` (mandatory) and
`--keyword`. The `--name` parameter should contain the full name of the
citizen whose CPF you want to discover. If this full name is unique in the
database, the script will handle downloading and parsing the partial CPF
provided by the Portal da Transparência. Based on this partial CPF, the script
generates all possible combinations, finds those valid according to the CPF
validation algorithm described above, and then attempts, through brute force,
to make a series of requests based on this generated and validated CPF. If
the CPF exists in the database, the script notifies. The program stops when
the found full name matches the name passed via the `--name` parameter.


For example, suppose you want to find the CPF of the president of Brazil, Mr.
Luiz Inácio Lula da Silva:

```bash
python script.py  --name "LUIZ INACIO LULA DA SILVA"
```

After perform many attempts, the script will report all found CPFs in Portal
da Transparência and then stops when the discovered CPF will correspond to
the same name passed through `--name`.

Parameter `--keyword`: when the full name of the citizen whose CPF you want
to discover is unique in the database, the above command is sufficient.
However, in some cases, there may be homonymous or very similar names. In
these cases, it is possible to pass the pattern of the partial CPF provided
by the Transparency Portal itself (e.g., `***.680.938-**`). In this case,
you should provide the full name (i.e., parameter --name) as well as the
`--keyword` parameter. Thus, the --keyword parameter will be used as the
search criterion, and the `--name parameter as the stop criterion.

For instance, suppose you want to discover the complete CPF of the former
president of Brazil, Ms. Dilma Vana Rousseff, knowing that part of her CPF is
`***.267.246-**`, as provided by the
[Portal da Transparência](https://portaldatransparencia.gov.br/pessoa-fisica/busca/lista?):

```bash
python script.py  --name "DILMA VANA ROUSSEFF" --keyword "***.267.246-**"
```

Example of execution of this script available in the video: [https://youtu.be/c13g8o0wMJs](https://youtu.be/c13g8o0wMJs).
