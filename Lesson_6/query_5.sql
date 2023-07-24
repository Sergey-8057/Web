SELECT t.fullname, sbj.name
FROM teachers t 
JOIN subjects sbj ON sbj.teacher_id = t.id
WHERE t.id = 1 --выбор преподавателя для сортировки
ORDER BY t.fullname;