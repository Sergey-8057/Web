SELECT g.date_of as [Date], gr.name as [Group], sbj.name as Subject, 
s.fullname as Students, g.grade as Grade
FROM grades g
JOIN subjects sbj ON sbj.id = g.subject_id
JOIN students s ON s.id = g.student_id
JOIN groups gr ON gr.id = s.group_id
WHERE g.date_of = '2023-05-30' and gr.id = 3 and sbj.id = 1; --выбор даты, группы и предмета для сортировки