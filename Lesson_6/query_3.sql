SELECT sbj.name, gr.name, ROUND(AVG(g.grade), 2) as avg_grade
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN subjects sbj ON sbj.id = g.subject_id 
JOIN groups gr ON gr.id = s.group_id
WHERE sbj.id = 2 --выбор предмета для сортировки
GROUP BY gr.id
ORDER BY avg_grade DESC;