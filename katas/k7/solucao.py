import math

def calcular_tarifa(minutos: int, tipo_veiculo: str) -> float:
    # Padroniza o texto para evitar problemas com maiúsculas/minúsculas
    tipo = tipo_veiculo.lower().strip()
    
    # Validação do tipo de veículo
    if tipo not in ['carro', 'moto']:
        raise ValueError("Tipo de veículo inválido. Use apenas 'carro' ou 'moto'.")
    
    # Aplicação da tolerância de 15 minutos
    minutos_cobrados = max(0, minutos - 15)
    
    # Se o tempo dentro da cobrança for 0, não há valor a pagar
    if minutos_cobrados == 0:
        return 0.0
    
    # Arredonda as horas para cima (ex: 75 min cobrados -> 1.25h -> 2h)
    horas_cobradas = math.ceil(minutos_cobrados / 60)
    
    # Cálculo por tipo de veículo
    if tipo == 'moto':
        return horas_cobradas * 5.0
    else:  # carro
        return horas_cobradas * 8.0