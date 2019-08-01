DECLARE @d1 int = :date_start, @d2 int = :date_end;  

SELECT
DBO.DateToShortDateStr(OP.DATETIME) AS datepay,
dbo.DateToShortTimeStr(op.DATETIME) as timepay,
op.COLUMN1 as numpko,
(CASE	WHEN OP.COLUMN2 = 0 THEN 'Текст'
		WHEN OP.COLUMN2 = 1 THEN 'Текст2'
		WHEN OP.COLUMN2 = 2 THEN 'Текст3'
		WHEN OP.COLUMN2 >= 3 THEN 'Текст4' END) AS typepay,
O.COLUMN3 as fullname,
O.COLUMN4 as numdoc,
DBO.DateToShortDateStr(O.DATETIME) AS datecontr,
dbo.DateToShortTimeStr(O.DATETIME) as timecontr,
OP.COLUMN5 as costall,
rpr.COLUMN6,
OP.COLUMN7 as rpnamepay,
RP.COLUMN8 as rpnamecontr,
ISNULL((D.COLUMN9),'') as department
FROM TABLE O 
LEFT JOIN TABLE2 OP ON  O.ID = OP.COLUMN10
LEFT JOIN TABLE3 RP ON (CASE WHEN o.COLUMN9 = 0 THEN O.COLUMN7 ELSE O.COLUMN9 END) = RP.ID
LEFT JOIN TABLE3 RPR on rpr.id = op.COLUMN7
LEFT JOIN TABLE4 D ON O.DEPARTMENT = D.ID
WHERE FLOOR(OP.DATETIME) BETWEEN @d1 AND @d2
ORDER BY op.DATETIME
