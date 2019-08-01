USE [msdb]
GO
EXEC msdb.dbo.sp_update_job @job_id=N'2bc5e5b0-2bf7-4a1d-a826-755a2d', 
		@notify_level_email=2, 
		@notify_level_page=2
GO 
EXEC msdb.dbo.sp_attach_schedule @job_id=N'2bc5e5b0-2bf7-4a1d-a826-755a2d',@schedule_id=11 
GO
---------------------------------------
USE DataBase 
DECLARE @ReleasePlaceFrom DT_REF 
DECLARE @ReleasePlaceTo DT_REF  
DECLARE @MaxInt DT_Integer0  
SET @ReleasePlaceFrom = 93 
SET @ReleasePlaceTo = 60  
SELECT @MaxInt = max(COLUMN1) FROM TABLE1 WHERE COLUMN2 = 1 AND COLUMN3 = 1 AND COLUMN4 = @ReleasePlaceTo 
IF EXISTS (SELECT * FROM TABLE2 WHERE COLUMN3 = 1 AND (ID = @ReleasePlaceFrom OR ID = @ReleasePlaceTo)) 
 BEGIN
  DECLARE @OrderID DT_REF
  DECLARE Cur CURSOR 
  LOCAL STATIC FORWARD_ONLY 
  FOR SELECT ID
  FROM TABLE1                   
	WHERE	COLUMN3 = 1 AND
	COLUMN4 <> 60 AND
	FLOOR(DATETIME) > 42430 AND
	COLUMN2 = 0 AND 
	(FLOOR(DATETIME) + COLUMN5 - (CASE WHEN COLUMN6 = 0 THEN COLUMN6 ELSE 1 END)) - (FLOOR(dbo.DateStrToDate('now'))) < 0 AND 
	OrderStatus = 4 AND 
	POID <> 62            
  OPEN Cur               
  FETCH NEXT FROM Cur INTO @OrderID      
  WHILE @@FETCH_STATUS = 0 
   BEGIN 
    SELECT @MaxInt = max(COLUMN1) FROM TABLE1 WHERE COLUMN2 = 1 AND COLUMN3 = 1 AND COLUMN4 = @ReleasePlaceTo 
    UPDATE TABLE1 SET              
     COLUMN7 = COLUMN4,              
     COLUMN8 = COLUMN9,    
     COLUMN4 = @ReleasePlaceTo,              
     COLUMN10 = @ReleasePlaceFrom,  
     COLUMN9 = @ReleasePlaceTo,               
     COLUMN11 = 'Auto',                           
     COLUMN12 = COLUMN13,              
     COLUMN2 = 1,                                   
     DATETIME2 = dbo.datestrtodate('now'),       
     DATETIME3 = dbo.datestrtodate('now'),     
     COLUMN1 = IsNull(@MaxInt, 0) + 1,     
	 COLUMN13 = 'ТЕКСТ' + CONVERT(VARCHAR(10),GETDATE(),104) + ' ' + COLUMN13   
    WHERE ID = @OrderID              
    FETCH NEXT FROM Cur INTO @OrderID  
   END 
 END 
