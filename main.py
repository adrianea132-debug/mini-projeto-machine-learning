from funcoes import (
    ler_csv,
    tratar_nulos_produtos,
    validar_regra_cancelamento,
    formatar_datas_pedidos,
    gerar_relatorio,
)

CAMINHO_PRODUTOS = "olist_products_dataset.csv"
CAMINHO_PEDIDOS = "olist_orders_dataset.csv"


def main():
    produtos = ler_csv(CAMINHO_PRODUTOS)
    pedidos = ler_csv(CAMINHO_PEDIDOS)

    produtos, nulos_corrigidos = tratar_nulos_produtos(produtos)

    resultado_cancelamento = validar_regra_cancelamento(pedidos)
    total_confirmados = len(resultado_cancelamento["confirmados"])
    total_excecoes = len(resultado_cancelamento["excecoes"])

    print(f"\nPedidos sem data de entrega e cancelados (hipótese confirmada): {total_confirmados}")
    print(f"Pedidos sem data de entrega mas NÃO cancelados (exceções): {total_excecoes}\n")

    pedidos = formatar_datas_pedidos(pedidos, coluna="order_approved_at")

    gerar_relatorio(
        total_produtos=len(produtos),
        total_pedidos=len(pedidos),
        nulos_corrigidos=nulos_corrigidos,
        total_cancelados=total_confirmados,
    )


if __name__ == "__main__":
    main()