from banco import session

def adicionar_fornecedor_no_banco(fornecedor):
    with session:
        session.add(fornecedor)
        session.commit()