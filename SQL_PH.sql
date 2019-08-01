DECLARE @Photo_id int, @Photo_client nvarchar(max), @Client_id int;
DECLARE Cur CURSOR
	
  FOR SELECT ID FROM TABLE1 where PHOTO is not null 
BEGIN
  OPEN Cur
  FETCH NEXT FROM Cur 
	INTO @Client_id
  WHILE @@FETCH_STATUS = 0 
   BEGIN
		SET @Photo_client  = CAST(@Client_id as nvarchar(10)) + '.png'
		exec [AKSFINANCE.AIS].dbo.ArchiCredit_PhotoExport @Client_id, 'E:\PHOTO', @Photo_client
    FETCH NEXT FROM Cur INTO @Client_id
   END
END
CLOSE Cur
DEALLOCATE Cur