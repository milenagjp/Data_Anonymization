create procedure omit(@table varchar(225), @column varchar(225))
AS 
begin
declare @FullQuery nvarchar(max), @sql nvarchar(max)
SET NOCOUNT ON;  
	
	exec(N'SELECT * INTO [Anonymized_' + @table + '] FROM '+@table+'' )

	exec(N'ALTER TABLE [Anonymized_' + @table + '] DROP COLUMN ' + @column + '')

SET NOCOUNT OFF; 
end
GO

