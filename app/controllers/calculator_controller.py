from flask import request, render_template
from ..models import EntrySAC

def sac_system_calculation(principal_value, months, interest_rate):
    """Retorna a tabela SAC, juros totais e montante"""
    
    amortization = EntrySAC.calculate_amortization(principal_value, months)

    total_interest = EntrySAC.calculate_total_interest(
        principal_value,
        months,
        interest_rate
    )

    tabela = []
    saldo = principal_value

    for mes in range(1, months + 1):
        juros = saldo * (interest_rate / 100)
        prestacao = amortization + juros
        saldo -= amortization

        tabela.append({
            "mes": mes,
            "amortizacao": amortization,
            "juros": juros,
            "prestacao": prestacao,
            "saldo_devedor": max(saldo, 0)
        })

    total_amount = principal_value + total_interest

    return tabela, total_interest, total_amount
