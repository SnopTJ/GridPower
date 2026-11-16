"""Funções de formatação de texto."""


def formatar_reais(valor):
    """Formata um número no padrão brasileiro: 18500 -> 'R$ 18.500,00'."""
    texto = f"{valor:,.2f}"                       # 18,500.00
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"R$ {texto}"
