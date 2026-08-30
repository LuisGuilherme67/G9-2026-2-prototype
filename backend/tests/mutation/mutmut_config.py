"""
Configuração para testes de mutação com Mutmut.
Garante alta resiliência e cobertura efetiva dos testes do domínio.
"""

def init():
    pass

def pre_mutation(context):
    # Ignora mutações em arquivos de configuração ou testes
    if "test_" in context.filename or "config.py" in context.filename:
        context.skip = True
