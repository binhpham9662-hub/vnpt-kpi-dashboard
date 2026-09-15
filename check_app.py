with open('app.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'Trung tâm Viễn thông Đông Anh' in line or 'brcd_agg' in line or 'TỔNG' in line:
            print(f'{i}: {line.strip()}')
