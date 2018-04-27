#%% Импортируем библиотеки

import pandas as pd
import numpy as np
import datetime

# Импортируем данные о продажах
initial_df = pd.read_excel('DeepRecommender/data_utils/sales/google_dataset.xlsx')

# Импортируем данные о привязке кодов к моделям
codes_models = pd.read_excel('DeepRecommender/data_utils/sales/код_модель.xlsx')

# Добавляем код модели в initial_df id модели
initial_df = initial_df.merge(codes_models, on='code')


#%% Формируем список уникальных клиентов, присваиваем каждому client_id
#   Добавляем client_id клиента в initial df

customers = pd.DataFrame(initial_df['client_name'].unique())
customers = customers.rename(columns={0: 'client_name'})
customers['client_id'] = range(1, len(customers) + 1)

# Добавляем client_id клиента в initial df
initial_df = initial_df.merge(customers, on='client_name')

# Удаляем ненужные столбцы (client_google_code, code)
initial_df = initial_df.iloc[:, 2:6]

#%% Понизим размерность данных, объединив транзакции, совершенные в течение трех дней

initial_df['Date'] = (initial_df['Date'] // 100).astype(int) * 100 +\
                     ((initial_df['Date'] % 100).astype(int) - ((initial_df['Date'] % 100).astype(int) - 1) % 3)


#%% проходим циклом по транзакциям

client_index = 1

skipped = 0

sales_updated_all = []

for customer_index, customer_row in customers.iterrows():
#for client_id in range(14, 15):

    client_id = customer_row[1]

    # Получаем список всех транзакций, выполненных клиентом
    client_df = initial_df[initial_df.client_id == client_id]
    # Сортируем по дате и сумме покупки
    client_df = client_df.sort_values(by=['Date', 'sum'], ascending=[True, False])

    # получаем список уникальных транзакций
    transactions = pd.DataFrame(client_df['Date'].unique())

    # Если клиент проводил только одну транзакцию, в течение которов покупал товар только одной модели,
    # Он не интересен для обучения
    if len(transactions) == len(pd.DataFrame(client_df['model_id'].unique())) == 1:
        skipped += 1
        continue

    sales_updated = []

    for i, r in transactions.iterrows():
        current_date = str(r[0])

        # каждая транзакция порождает новый список, в котором дата текущей итерации является нулевой точкой
        unique_models_list = []

        transactions_list = []

        for index, row in client_df.iterrows():
            date = str(int(row['Date']))

            model = row['model_id']
            client = row['client_id']
            summary = row['sum']

            # Количество дней между датой и нулевой точкой
            days = (datetime.datetime.strptime(date, '%Y%m%d') - datetime.datetime.strptime(current_date, '%Y%m%d')).days

            # Количество полных месяцев между датой и нулевой точкой
            months = abs(days // 30.4)
            delta = abs(days % 30.4)

            model_1 = ''
            model_2 = ''
            probability_1 = ''
            probability_2 = ''

            if days == 0:
                model_1 = int(model)
                probability_1 = 1
                unique_models_list.append(model_1)
            elif days < 0:
                model_1 = int(model * (-1) - 10000 * (months - 1))
                probability_1 = 1 - delta / 30.4
                model_2 = int(model * (-1) - 10000 * months)
                probability_2 = delta / 30.4
                unique_models_list.append(model_1)
                unique_models_list.append(model_2)
            else:
                model_1 = int(model + 10000 * months)
                probability_1 = delta / 30.4
                model_2 = int(model + 10000 * (months + 1))
                probability_2 = 1 - delta / 30.4
                unique_models_list.append(model_1)
                unique_models_list.append(model_2)

            if -10000 < model_1 < 0:
                model_1 = model_1 * (-1)


            if model_2 == '':
                probability_1 = float(probability_1) * 5
                transactions_list.append({'client_id': client_index, 'model_id': model_1, 'probability': probability_1})
            else:
                probability_1 = float(probability_1) * 5
                probability_2 = float(probability_2) * 5
                transactions_list.append({'client_id': client_index, 'model_id': model_1, 'probability': probability_1})
                transactions_list.append({'client_id': client_index, 'model_id': model_2, 'probability': probability_2})

        client_index = client_index + 1
        transactions_df = pd.DataFrame(transactions_list).drop_duplicates(subset=['model_id'])
        sales_updated.append(transactions_df)

    sales_updated_all.append(pd.concat(sales_updated))

print(skipped)


#%% Concat all customers

sales_updated_all_in_one = pd.concat(sales_updated_all)

sales_updated_all_in_one.to_csv('DeepRecommender/data_utils/sales/SALES_MONTH_SPLIT_ALL.csv', sep='\t', encoding='utf-8', index=False)


#%%

print(pd.DataFrame(sales_updated_all_in_one['model_id'].unique()))
