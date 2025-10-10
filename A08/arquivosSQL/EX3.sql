DROP VIEW IF EXISTS view_enade; 
go
CREATE VIEW view_enade as
SELECT
	a.descricao as area, curso.nome as curso, avg(enade) as media_enade
FROM Cursos_Oferecidos_por_Campus c
INNER JOIN Area a on a.id_area = c.id_area
INNER JOIN Curso curso on curso.id_curso = c.id_curso
group by a.descricao, curso.nome
having avg(enade) >= 3;