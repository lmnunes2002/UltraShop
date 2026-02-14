from typing import List, Optional

def get_pagination_list(
    current_page: int,
    total_pages: int,
    left_edge: int = 1,
    right_edge: int = 1,
    left_current: int = 1,
    right_current: int = 2
) -> List[Optional[int]]:
    
    items = []
    last_num = 0

    for num in range(1, total_pages + 1):
        if (
            num <= left_edge
            or num > total_pages - right_edge
            or (current_page - left_current <= num <= current_page + right_current)
        ):
            if last_num + 1 != num:
                items.append(None)
            
            items.append(num)
            last_num = num
            
    return items