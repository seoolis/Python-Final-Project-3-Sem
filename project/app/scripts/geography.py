#querries
# Запрос для уровня зарплат по городам

'''SELECT
    area_name AS "Город",
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancy_table), 2) AS "Доля вакансий в %"
FROM vacancy_table
GROUP BY area_name
ORDER BY COUNT(*) DESC
LIMIT 15;'''

# Запрос для уровня зарплат по городам (для выбранной профессии)
'''SELECT
    area_name AS "Город",
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancy_table WHERE name ILIKE ANY (ARRAY['%backend%', '%бэкэнд%', '%бэкенд%', '%бекенд%', '%бэкэнд%', '%back end%', '%бэк энд%', '%бэк енд%'])), 2) AS "Доля вакансий в %"
FROM vacancy_table
WHERE name ILIKE ANY (ARRAY['%backend%', '%бэкэнд%', '%бэкенд%', '%бекенд%', '%бэкэнд%', '%back end%', '%бэк энд%', '%бэк енд%'])
GROUP BY area_name
ORDER BY COUNT(*) DESC
LIMIT 15;'''

