create procedure [default](@table varchar(225), @column varchar(225))
AS 
begin
declare @FullQuery nvarchar(max), @sql nvarchar(max)
SET NOCOUNT ON;  
	
	exec(N'SELECT * INTO [Anonymized_' + @table + '] FROM '+@table+'')

	exec(N'UPDATE [Anonymized_' + @table + '] SET ' + @column + '= (SELECT DISTINCT TOP 1 COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME = '+@column+' order by COLUMN_DEFAULT desc)')

	
SET NOCOUNT OFF; 
end
GO
