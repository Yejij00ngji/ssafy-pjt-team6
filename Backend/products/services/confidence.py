# open ai가 사용할 신뢰도 점수 계산
def calculate_confidence(target_score, all_scores):
    """
    추천 결과의 상대적 신뢰도 (0~1)
    """
    lower_count = sum(1 for s in all_scores if s < target_score)
    return round(lower_count / len(all_scores), 2)
