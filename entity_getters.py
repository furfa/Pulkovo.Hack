from entity_classes import *
import json

all_disciplines1 = [
    "Центровка и контроль загрузки",
    "Управление безопасностью полетов",
    "Опасные грузы",
    "Авиационная безопасность",
    "Аварийно-спасательное обеспечение полетов",
    "Противообледенительная защита воздушных судов",
    "Организация наземного обслуживания",
    "Организация пассажирских перевозок"
]

all_disciplines = [
    "Цент",
    "Упра",
    "Опас",
    "Авиа",
    "Авар",
    "Прот",
    "Орга",
    "Орга"
]

def read_teachers_json():
    f = open("./data/teachers.json", "r")
    result = json.load(f)
    f.close()
    return result

def read_programs_json():
    f = open("./data/parsed_programs.json", "r")
    result = json.load(f)
    f.close()
    return result

def get_teachers():
    
    return [
        Teacher(
            id=0,
            allowed_tasks=[ (0, 6), (4, 6), (1, 4), (5, 5) ],
            allowed_times=[ 1, 2, 3, 4 ],
            name="Pasha(only 0 and 1 lessons)"
        ),
        Teacher(
            id=1,
            allowed_tasks=[ (0, 1), (1, 5), (2, 3), (3, 4) ],
            allowed_times=[ 0, 1, 2, 3, 4 ],
            name="Masha(1st-discipline, all)"
        ),
        Teacher(
            id=2,
            allowed_tasks=[ (1, 4), (2, 4), (3, 5) ],
            allowed_times=[ 0, 1, 2, 3, 4 ],
            name="Vitya(1st-discipline, no base)"
        ),
        Teacher(
            id=3,
            allowed_tasks=[ (4, 8), (5, 5), (6, 3), (7, 4) ],
            allowed_times=[ 0, 1, 2, 3, 4 ],
            name="Olga(2nd-discipline, all)"
        ),
        Teacher(
            id=4,
            allowed_tasks=[ (5, 4), (6, 4), (7, 5) ],
            allowed_times=[ 0, 1, 2, 3, 4 ],
            name="Kolya(2nd-discipline, no base)"
        ),
        Teacher(
            id=5,
            allowed_tasks=[ (3, 6), (7, 6) ],
            allowed_times=[ 0, 1, 2, 3, 4 ],
            name="Practical_Mega_Boss(only practice)"
        )
    ]


def get_tasks():
    return [
        Task(0, all_disciplines[0], "Base", False),
        Task(1, all_disciplines[0], "Simple", False, 0),
        Task(2, all_disciplines[0], "Simple", False, 1),
        Task(3, all_disciplines[0], "Simple", True, 2),
        Task(4, all_disciplines[1], "Base", False),
        Task(5, all_disciplines[1], "Simple", False, 4),
        Task(6, all_disciplines[1], "Simple", False, 5),
        Task(7, all_disciplines[1], "Simple", True, 6),
    ]
def get_audiences():
    return [
        #Base non practice
        Audience(
            id=0,
            tasks_allowed=[ (0, 2), (1, 1), (2, 1), (4, 2), (5, 1), (6, 1) ]
        ),
        # All non practice (non base)
        Audience(
            id=1,
            tasks_allowed=[ (0, 1), (1, 2), (2, 2), (4, 1), (5, 2), (6, 2) ]
        ),
        # Only practice
        Audience(
            id=2,
            tasks_allowed=[ (3, 2), (7, 2) ]
        ),
    ]

def get_times():
    return [
        Time(
            id=0,
            start=datetime(2020, 9, 1, 8, 0, 0),
            end=datetime(2020, 9, 1, 9, 30, 0)
        ),
        Time(
            id=1,
            start=datetime(2020, 9, 1, 10, 0, 0),
            end=datetime(2020, 9, 1, 11, 30, 0)
        ),
        Time(
            id=2,
            start=datetime(2020, 9, 1, 12, 0, 0),
            end=datetime(2020, 9, 1, 13, 30, 0)
        ),
        Time(
            id=3,
            start=datetime(2020, 9, 2, 8, 0, 0),
            end=datetime(2020, 9, 2, 9, 30, 0)
        ),
        Time(
            id=4,
            start=datetime(2020, 9, 2, 10, 0, 0),
            end=datetime(2020, 9, 2, 11, 30, 0)
        ),
        Time(
            id=5,
            start=datetime(2020, 9, 2, 12, 0, 0),
            end=datetime(2020, 9, 2, 13, 30, 0)
        ),
        # Time(
        #     id=6,
        #     start=datetime(2020, 9, 3, 8, 0, 0),
        #     end=datetime(2020, 9, 3, 9, 30, 0)
        # ),
        # Time(
        #     id=7,
        #     start=datetime(2020, 9, 3, 10, 0, 0),
        #     end=datetime(2020, 9, 3, 11, 30, 0)
        # ),
        # Time(
        #     id=8,
        #     start=datetime(2020, 9, 3, 12, 0, 0),
        #     end=datetime(2020, 9, 3, 13, 30, 0)
        # ),
    ]