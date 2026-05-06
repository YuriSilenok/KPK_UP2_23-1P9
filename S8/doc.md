# Сервис подгрупп (Subgroup Service) - Вариант 8

## Предметная область
Управление делением учебных групп на подгруппы (для занятий по иностранному языку, физкультуре, лабораторным работам и т.д.). Одна группа может делиться на несколько подгрупп. В одной подгруппе могут учиться несколько студентов. Студент может входить только в одну подгруппу в рамках одного типа деления.

## ER-диаграмма (3НФ, многие-ко-многим через транзитивную таблицу)

```mermaid
erDiagram
    SUBGROUP {
        int id PK
        int group_id FK
        string name
        string type "лекционная/практическая/лабораторная"
        int max_students
    }
    
    STUDENT {
        int id PK
        string first_name
        string last_name
        string email
    }
    
    GROUP {
        int id PK
        string name
        int formation_year
        string status
    }
    
    SUBGROUP_STUDENT {
        int id PK
        int subgroup_id FK
        int student_id FK
        date joined_at
    }
    
    GROUP ||--o{ SUBGROUP : "имеет"
    SUBGROUP ||--o{ SUBGROUP_STUDENT : "содержит"
    STUDENT ||--o{ SUBGROUP_STUDENT : "входит в"