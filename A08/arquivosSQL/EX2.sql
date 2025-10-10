drop view if exists view_curso;
go
create view view_curso as
select
    c.nome,
    count(*) as ofertas
from Curso c
inner join Cursos_Oferecidos_por_Campus o on c.id_curso = o.id_curso
group by c.nome
having count(*) >= 2000;
go