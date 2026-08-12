import csv
import re
from datetime import datetime


def ler_csv(caminho_arquivo):
    linhas = []
    with open(caminho_arquivo, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            linhas.append(linha)
    return linhas


def limpar_texto_categoria(texto):
    if texto is None:
        return ""
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9_\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def calcular_media_coluna(produtos, coluna):
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
    colunas_dimensoes = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

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
                produto[coluna] = round(medias[coluna], 2)
                total_nulos_corrigidos += 1

    return produtos, total_nulos_corrigidos


def validar_regra_cancelamento(pedidos):
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
    if data_str in (None, ""):
        return ""
    try:
        data_obj = datetime.strptime(data_str.strip(), formato_original)
        return data_obj.strftime("%d/%m/%Y")
    except ValueError:
        return ""


def formatar_datas_pedidos(pedidos, coluna="order_approved_at"):
    for pedido in pedidos:
        pedido[coluna] = converter_data_para_br(pedido.get(coluna, ""))
    return pedidos


def gerar_relatorio(total_produtos, total_pedidos, nulos_corrigidos, total_cancelados):
    print("=" * 50)
    print("RELATÓRIO DE SANITIZAÇÃO - OLIST")
    print("=" * 50)
    print(f"Total de produtos processados:        {total_produtos}")
    print(f"Total de pedidos processados:         {total_pedidos}")
    print(f"Total de registros nulos corrigidos:  {nulos_corrigidos}")
    print(f"Total de pedidos cancelados (hipótese confirmada): {total_cancelados}")
    print("=" * 50)