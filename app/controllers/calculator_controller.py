from flask import Blueprint, request, jsonify
from ..models import EntrySAC

def sac_system_calculation():
    """Simula o Sistema de Amortização Constante (SAC) e gera uma tabela HTML"""
    try:
        # Coleta dados do formulário
        principal_value = float(request.form['principal_value'])
        months = int(request.form['months'])
        interest_rate = float(request.form['interest_rate'])

        # --- Usa os métodos prontos da classe EntrySAC --- #
        amortization = EntrySAC.calculate_amortization(principal_value, months)
        total_interest = EntrySAC.calculate_total_interest(principal_value, months, interest_rate)
        payments = EntrySAC.calculate_payments(principal_value, months, interest_rate)

        # Monta tabela detalhada mês a mês
        tabela = []
        saldo = principal_value
        for mes in range(1, months + 1):
            juros = saldo * (interest_rate / 100)
            prestacao = amortization + juros
            saldo -= amortization
            tabela.append({
                "mes": mes,
                "amortizacao": f"{amortization:,.2f}",
                "juros": f"{juros:,.2f}",
                "prestacao": f"{prestacao:,.2f}",
                "saldo_devedor": f"{max(saldo, 0):,.2f}"
            })

        total_amount = principal_value + total_interest

        # Renderiza o template com os dados
        return render_template(
            "sac.html",
            tabela=tabela,
            capital_inicial=f"{principal_value:,.2f}",
            juros_totais=f"{total_interest:,.2f}",
            montante=f"{total_amount:,.2f}",
            prazo=months,
            taxa_juros=interest_rate
        )

    except Exception as e:
        return render_template("sac.html", erro=str(e))



