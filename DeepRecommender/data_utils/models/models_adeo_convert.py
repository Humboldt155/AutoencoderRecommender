import pandas as pd

# Получаем данные о модели
models_adeo = pd.read_excel('MODELS_ADEO.xlsx')


# Каждая модель получает 24 своих копии.
# В новом ID Закодирована информация о месяце до или после текущего момента. Коэффициент = 10000 * (месяц до или после)
# Например, модель с индексом 125 получает копии 60125 (+6 месяцев), -30125 (-3 месяцев) и т.д.
# Аналогичным образом выполнено разделение по кварталам

# По месяцам
models_list_m = []
for i in range(-120000, 130000, 10000):
    for index, row in models_adeo.iterrows():
        model_initial_id = row['model_id']
        model_code = row['model_code']
        model_name = row['model_name']
        model_month = (i / 10000)

        if i < 0:
            model_id = model_initial_id * (- 1) + i
        elif i > 0:
            model_id = model_initial_id + i
        else:
            model_id = model_initial_id

        new_row = {
            'model_id': model_id,
            'model_initial_id': model_initial_id,
            'model_code': model_code,
            'model_name': model_name,
            'model_month': model_month
        }
        models_list_m.append(new_row)

models_up_m = pd.DataFrame(models_list_m)

models_up_m.to_csv('MODELS_ADEO_MONTH_SPLIT.csv', sep='\t', encoding='utf-8', index=False)

# По кварталам
models_list_q = []
for i in range(-40000, 50000, 10000):
    for index, row in models_adeo.iterrows():
        model_initial_id = row['model_id']
        model_code = row['model_code']
        model_name = row['model_name']
        model_quarter = (i / 10000)

        if i < 0:
            model_id = model_initial_id * (- 1) + i
        elif i > 0:
            model_id = model_initial_id + i
        else:
            model_id = model_initial_id

        new_row = {
            'model_id': model_id,
            'model_initial_id': model_initial_id,
            'model_code': model_code,
            'model_name': model_name,
            'model_quarter': model_quarter
        }
        models_list_q.append(new_row)

models_up_q = pd.DataFrame(models_list_q)

models_up_q.to_csv('MODELS_ADEO_QUARTER_SPLIT.csv', sep='\t', encoding='utf-8', index=False)
