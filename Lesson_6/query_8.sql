SELECT t.fullname as Teacher, sbj.name as Subject, ROUND(AVG(g.grade), 2) as Avg_grade
FROM teachers t
JOIN subjects sbj ON teacher_id = t.id 
JOIN grades g ON g.subject_id = sbj.id
WHERE t.id = 1 --выбор преподавателя для сортировки
GROUP BY g.subject_id;