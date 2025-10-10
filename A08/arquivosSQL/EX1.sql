DROP VIEW IF EXISTS view_uf;
go
CREATE VIEW view_uf AS
SELECT distinct
	m.uf as unidade_federativa
FROM Municipio m;