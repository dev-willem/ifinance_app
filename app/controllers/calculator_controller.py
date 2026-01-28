from flask import request, render_template, jsonify
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


def sac_system_api():
    """Endpoint API para cálculo SAC: aceita form ou JSON e retorna JSON com tabela e totais."""
    try:
        data = request.get_json() or request.form
        principal_value = float(data.get('principal_value'))
        months = int(data.get('months'))
        interest_rate = float(data.get('interest_rate'))

        tabela, total_interest, total_amount = sac_system_calculation(principal_value, months, interest_rate)

        return jsonify({
            'tabela': tabela,
            'juros_totais': total_interest,
            'montante': total_amount
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def price_system_calculation(principal_value, months, interest_rate):
    """Retorna a tabela PRICE (sistema francês), juros totais e montante"""
    r = interest_rate / 100.0
    tabela = []
    if r == 0:
        prestacao = round(principal_value / months, 2)
    else:
        prestacao = round(principal_value * (r * (1 + r) ** months) / ((1 + r) ** months - 1), 2)

    saldo = principal_value
    total_interest = 0.0

    for mes in range(1, months + 1):
        juros = round(saldo * r, 2)
        amortizacao = round(prestacao - juros, 2)
        saldo = round(saldo - amortizacao, 2)
        if saldo < 0:
            saldo = 0.0

        tabela.append({
            "mes": mes,
            "amortizacao": amortizacao,
            "juros": juros,
            "prestacao": prestacao,
            "saldo_devedor": saldo,
        })

        total_interest += juros

    total_interest = round(total_interest, 2)
    total_amount = round(principal_value + total_interest, 2)
    return tabela, total_interest, total_amount


def credit_system_calculation(principal_value, months, interest_rate):
    """Simulação de crédito — por padrão usa o sistema PRICE (parcelas constantes)."""
    return price_system_calculation(principal_value, months, interest_rate)


def fixed_income_simulation(principal_value, months, interest_rate):
    """Simulação de renda fixa com capitalização composta mensal.
    Retorna lista de saldos mensais, juros totais e montante final.
    """
    r = interest_rate / 100.0
    tabela = []
    saldo = principal_value

    for mes in range(1, months + 1):
        juros = round(saldo * r, 2)
        saldo = round(saldo + juros, 2)
        tabela.append({
            "mes": mes,
            "juros": juros,
            "saldo": saldo,
        })

    total_interest = round(saldo - principal_value, 2)
    total_amount = saldo
    return tabela, total_interest, total_amount


def profit_simulation(revenue, fixed_costs, variable_costs, taxes):
    """Simulação de lucro simples: calcula lucro líquido e margens."""
    revenue = float(revenue)
    fixed_costs = float(fixed_costs)
    variable_costs = float(variable_costs)
    taxes = float(taxes)

    gross_profit = revenue - (fixed_costs + variable_costs)
    net_profit = gross_profit - taxes

    margin_gross = round((gross_profit / revenue) * 100, 2) if revenue else 0.0
    margin_net = round((net_profit / revenue) * 100, 2) if revenue else 0.0

    return {
        "revenue": round(revenue, 2),
        "fixed_costs": round(fixed_costs, 2),
        "variable_costs": round(variable_costs, 2),
        "taxes": round(taxes, 2),
        "gross_profit": round(gross_profit, 2),
        "net_profit": round(net_profit, 2),
        "margin_gross": margin_gross,
        "margin_net": margin_net,
    }


def cet_calculation(principal_value, months, interest_rate, admin_fees=0.0, insurance=0.0, taxes=0.0):
    """Cálculo simplificado do CET: soma todos os custos e expressa como percentual do principal.
    Retorna a tabela mensal (simples), custo total e CET percentual.
    """
    # Reaproveita cálculo de juros (PRICE) para total de juros
    tabela, total_interest, _ = price_system_calculation(principal_value, months, interest_rate)
    total_fees = float(admin_fees) + float(insurance) + float(taxes)
    total_costs = round(total_interest + total_fees, 2)

    cet_percent_total = round((total_costs / principal_value) * 100, 2) if principal_value else 0.0

    return tabela, total_costs, cet_percent_total
