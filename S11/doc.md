\# Вариант 11: Discipline Service (Сервис дисциплин)



\## 1. Список функций



\### Добавить дисциплину

| Параметр | Обязательность | Тип | Ограничение |

| :--- | :--- | :--- | :--- |

| `name` | Да | String | Уникальное |

| `code` | Да | String | Уникальное |

| `total\_hours` | Да | Integer | > 0 |

| `category\_id` | Да | Integer | Not NULL |



\## 2. ER-диаграмма

```mermaid

erDiagram

   CATEGORY ||--|{ DISCIPLINE : "содержит"

   CATEGORY {

      int id PK

       string name

   }

   DISCIPLINE {

       int id PK

       string name

      string code

       int total\_hours

       int category\_id FK

   }

