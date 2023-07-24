SELECT sbj.name, s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN subjects sbj ON sbj.id = g.subject_id 
WHERE sbj.id = 1 --выбор предмета для сортировки
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 1;