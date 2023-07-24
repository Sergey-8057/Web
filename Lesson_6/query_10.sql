SELECT DISTINCT t.fullname as Teacher, sbj.name as Subject, s.fullname as Student
FROM teachers t
JOIN subjects sbj ON teacher_id = t.id
JOIN grades g ON g.subject_id = sbj.id
JOIN students s ON s.id = g.student_id
WHERE t.id = 1 and s.id = 2 --выбор преподавателя и студента для сортировки
ORDER BY sbj.name;