SELECT DISTINCT s.fullname as Student, sbj.name as Subjects
FROM students s
JOIN grades g ON g.student_id = s.id
JOIN subjects sbj ON sbj.id = g.subject_id 
WHERE s.id = 2 --выбор студента для сортировки
ORDER BY sbj.name;