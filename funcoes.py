import csv
import re
from datetime import datetime


def ler_csv(caminho_arquivo):
    """
    Lê um arquivo CSV usando csv.DictReader, para que cada linha vire
    um dicionário (chave = nome da coluna, valor = conteúdo da célula).
    Usamos 'with open()' para garantir que o arquivo seja fechado
    automaticamente, mesmo se ocorrer algum erro durante a leitura.
    """
    linhas = []
    with open(caminho_arquivo, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            linhas.append(linha)
    return linhas


def limpar_texto_categoria(texto):
    """
    Padroniza o texto de uma categoria de produto:
    - .lower() para deixar tudo em letras minúsculas
    - .strip() para remover espaços em branco no início/fim
    - regex para remover caracteres especiais/pontuação indevida,
      mantendo apenas letras, números, underscore e espaços
    - regex extra para colapsar múltiplos espaços em um só
    """
    if texto is None:
        return ""
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9_\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def calcular_media_coluna(produtos, coluna):
    """
    Calcula a média dos valores numéricos válidos de uma coluna
    (ignorando vazios e valores que não conseguem ser convertidos
    para float). Essa média é usada depois para preencher os nulos
    das dimensões físicas dos produtos.
    """
    valores = []
    for produto in produtos:
        valor = produto.get(coluna, "")
        if valor not in (None, ""):
            try:
                valores.append(float(valor))
            except ValueError:
                continue
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


def tratar_nulos_produtos(produtos):
    """
    Trata os valores nulos/vazios da base de produtos:

    1) product_category_name: quando vazio, preenchemos com a string
       "sem categoria" (conforme exigido no enunciado). Quando não
       está vazio, aplicamos a padronização de texto (lower/strip/regex).

    2) Dimensões físicas (product_weight_g, product_length_cm,
       product_height_cm, product_width_cm): optamos por preencher
       os valores nulos com a MÉDIA da coluna, em vez de descartar o
       registro inteiro. Justificativa técnica: descartar a linha
       faria perder informações válidas de outras colunas do mesmo
       produto (ex: categoria, nome) só porque uma única dimensão
       está faltando. Usar a média é uma estimativa razoável, mantém
       o volume de dados da base e evita distorcer fortemente as
       estatísticas gerais, já que não criamos outliers artificiais.
    """
    colunas_dimensoes = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    # Calcula a média de cada coluna de dimensão ANTES de qualquer
    # substituição, para não contaminar o cálculo com valores que
    # nós mesmos vamos inserir.
    medias = {coluna: calcular_media_coluna(produtos, coluna) for coluna in colunas_dimensoes}

    total_nulos_corrigidos = 0

    for produto in produtos:
        categoria = produto.get("product_category_name", "")
        if categoria in (None, ""):
            produto["product_category_name"] = "sem categoria"
            total_nulos_corrigidos += 1
        else:
            produto["product_category_name"] = limpar_texto_categoria(categoria)

        for coluna in colunas_dimensoes:
            valor = produto.get(coluna, "")
            if valor in (None, ""):
                # Preenche o nulo com a média da coluna, arredondada
                # para 2 casas decimais, mantendo o registro na base.
                produto[coluna] = round(medias[coluna], 2)
                total_nulos_corrigidos += 1

    return produtos, total_nulos_corrigidos


def validar_regra_cancelamento(pedidos):
    """
    Regra de negócio: verifica se todo pedido sem
    order_delivered_customer_date está, de fato, com order_status
    igual a "canceled". Separamos os pedidos em duas listas:
    - confirmados: sem data de entrega E cancelados (hipótese válida)
    - excecoes: sem data de entrega, mas NÃO cancelados (hipótese
      quebrada nesses casos específicos)
    """
    confirmados = []
    excecoes = []

    for pedido in pedidos:
        data_entrega = pedido.get("order_delivered_customer_date", "")
        status = pedido.get("order_status", "").strip().lower()

        if data_entrega in (None, ""):
            if status == "canceled":
                confirmados.append(pedido)
            else:
                excecoes.append(pedido)

    return {
        "confirmados": confirmados,
        "excecoes": excecoes,
        "total_sem_data_entrega": len(confirmados) + len(excecoes),
    }


def converter_data_para_br(data_str, formato_original="%Y-%m-%d %H:%M:%S"):
    """
    Converte uma string de data do formato original do dataset
    (ex: "2017-05-16 15:05:35") para o formato brasileiro simplificado
    (ex: "16/05/2017"), usando o módulo datetime. Se a data vier vazia
    ou em um formato inesperado, retornamos string vazia em vez de
    quebrar o script.
    """
    if data_str in (None, ""):
        return ""
    try:
        data_obj = datetime.strptime(data_str.strip(), formato_original)
        return data_obj.strftime("%d/%m/%Y")
    except ValueError:
        return ""


def formatar_datas_pedidos(pedidos, coluna="order_approved_at"):
    """
    Aplica a conversão de data brasileira em todos os pedidos,
    para a coluna informada (por padrão, order_approved_at).
    """
    for pedido in pedidos:
        pedido[coluna] = converter_data_para_br(pedido.get(coluna, ""))
    return pedidos


def gerar_relatorio(total_produtos, total_pedidos, nulos_corrigidos, total_cancelados):
    """
    Exibe no terminal um resumo manual (sem bibliotecas externas)
    com as estatísticas finais do pipeline de sanitização, permitindo
    validar visualmente se a base foi processada corretamente.
    """
    print("=" * 50)
    print("RELATÓRIO DE SANITIZAÇÃO - OLIST")
    print("=" * 50)
    print(f"Total de produtos processados: {total_produtos}")
    print(f"Total de pedidos processados: {total_pedidos}")
    print(f"Total de registros nulos corrigidos: {nulos_corrigidos}")
    print(f"Total de pedidos cancelados (hipótese confirmada): {total_cancelados}")
    print("=" * 50)
