SELECT s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
FROM grades g 
JOIN students s ON s.id = g.student_id 
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 5;