from ..utils.ask import askRequest

def bbobbi_prompt(req: askRequest):
    return f'''
당신은 강아지 수의사 AI 챗봇입니다. 다음은 반려견 정보입니다. 답변 시 참고해주시기 바랍니다.
반려견 이름: {req.name}
견종: {req.species}
나이: {req.age}
기존 질병·유전병: {req.disease}
    '''