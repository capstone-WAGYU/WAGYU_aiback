from ..utils.ask import askRequest

def bbobbi_prompt(req: askRequest):
    return f'''
다음은 반려견 정보이다. 답변 시 자연스럽게 참고하여라.
반려견 이름: {req.name}
견종: {req.species}
    '''