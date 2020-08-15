import pandas as pd
import jellyfish
import json

def similar(a, b):
    return jellyfish.levenshtein_distance(a, b)

data = pd.read_excel("./Приложение №2.xlsx", sheet_name="параметры программ")
courses = [i for i in data["Учебная программа"]]

f = open("parsed_docx.json", "r")
fo = json.load(f)
f.close()
parsed_courses = [i for i in fo.keys()]

for pj in parsed_courses:
    if "DI-L10" in pj:
        continue
    similar_points = 1000000
    most_similar = ""
    for p in courses:
        cur_similar_points = similar(pj, p)
        if cur_similar_points < similar_points:
            similar_points = cur_similar_points
            most_similar = p
    tmp = fo[pj]
    del fo[pj]
    fo[most_similar] = tmp

with open("./parsed_docx_ref.json", "w") as f:
    json.dump(fo, f)