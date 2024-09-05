path_to_index = "init_data/flat.index"
# path_to_index = "/Users/pavelvyaznikov/Documents/ITMO_X5_HACKATHON/search_engine/init_data/flat.index"

path_to_excel = "init_data/x5_qa.csv"
# path_to_excel = "/Users/pavelvyaznikov/Documents/ITMO_X5_HACKATHON/search_engine/init_data/x5_qa.csv"
# path_to_testfile = "init_data/spec_final_val.csv"

healthcheck_timeout = 30
healthcheck_sleep = 5
topn = 10

abbr_decoding = {
    "лк": "личный кабинет",
    "БиР": "Беременность и роды",
    "зп": "заработная плата",
    "НДФЛ": "Налог на доходы физических лиц",
    "СТД": "срочный трудовой договор",
    "ТК": "трудовой договор",
    "АО": "авансовый отчет",
    "SLA": "сроки",
    "ЭЦП": "электронная цифровая подпись",
    "КР": "кадровый резерв",
}


def faiss_func(x):
    return f'Запрос: {x["question"]}; Ответ: {x["content"]}; Категория: {x["category"]}'
