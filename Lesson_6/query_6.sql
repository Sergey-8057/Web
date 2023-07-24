SELECT gr.name, s.fullname
FROM groups gr
JOIN students s ON s.group_id = gr.id
WHERE gr.id = 3 --выбор группы для сортировки
ORDER BY s.fullname;