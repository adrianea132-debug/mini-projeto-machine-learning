from funcoes import (
    ler_csv,
    tratar_nulos_produtos,
    validar_regra_cancelamento,
    formatar_datas_pedidos,
    gerar_relatorio,
)

# Caminhos dos arquivos de dados brutos da Olist. Devem estar na
# mesma pasta dos scripts para o pipeline funcionar.
CAMINHO_PRODUTOS = "olist_products_dataset.csv"
CAMINHO_PEDIDOS = "olist_orders_dataset.csv"


def main():
    # 1) Leitura dos arquivos CSV brutos, transformando cada linha
    # em um dicionário (lista de dicionários por arquivo).
    produtos = ler_csv(CAMINHO_PRODUTOS)
    pedidos = ler_csv(CAMINHO_PEDIDOS)

    # 2) Tratamento de nulos e padronização de texto na base de
    # produtos (categoria + dimensões físicas). Ver justificativa
    # técnica detalhada nos comentários de tratar_nulos_produtos().
    produtos, nulos_corrigidos = tratar_nulos_produtos(produtos)

    # 3) Validação da regra de negócio: pedidos sem data de entrega
    # devem estar, obrigatoriamente, com status "canceled".
    resultado_cancelamento = validar_regra_cancelamento(pedidos)
    total_confirmados = len(resultado_cancelamento["confirmados"])
    total_excecoes = len(resultado_cancelamento["excecoes"])

    print(f"\nPedidos sem data de entrega e cancelados (hipótese confirmada): {total_confirmados}")
    print(f"Pedidos sem data de entrega mas NÃO cancelados (exceções): {total_excecoes}\n")

    # 4) Conversão da coluna order_approved_at para o formato de
    # data brasileiro (dd/mm/aaaa).
    pedidos = formatar_datas_pedidos(pedidos, coluna="order_approved_at")

    # 5) Geração do relatório final com os totais processados.
    gerar_relatorio(
        total_produtos=len(produtos),
        total_pedidos=len(pedidos),
        nulos_corrigidos=nulos_corrigidos,
        total_cancelados=total_confirmados,
    )


if __name__ == "__main__":
    main()
