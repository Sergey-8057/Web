SELECT t.fullname as Teacher, s.fullname as Student, ROUND(AVG(g.grade), 2) as Avg_grade
FROM teachers t
JOIN subjects sbj ON sbj.teacher_id = t.id 
JOIN grades g ON g.subject_id = sbj.id
JOIN students s ON s.id = g.student_id
WHERE t.id = 2  and s.id = 4 --выбор преподавателя и студента для сортировки
GROUP BY g.student_id;