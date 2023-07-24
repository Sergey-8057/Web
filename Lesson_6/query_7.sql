SELECT gr.name as [Group], sbj.name as Subject, s.fullname as Students, g.grade as Grades
FROM groups gr
JOIN students s ON s.group_id = gr.id
JOIN grades g ON g.student_id = s.id
JOIN subjects sbj ON sbj.id = g.subject_id 
WHERE gr.id = 3 and sbj.id = 1 --выбор группы и предмета для сортировки
ORDER BY s.fullname;