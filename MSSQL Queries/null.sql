create procedure [null](@table varchar(225), @column varchar(225))
AS 
begin
declare @FullQuery nvarchar(max), @sql nvarchar(max)
SET NOCOUNT ON;
  
	exec(N'select * into [Anonymized_' + @table + '] from '+@table+'')
	exec(N'UPDATE [Anonymized_' + @table + '] SET ' + @column + ' = NULL')
	--set @FullQuery = N'UPDATE TABLE [#Anonymized_' + @table + '] SET ' + @column + ' = NULL'


SET NOCOUNT OFF; 
end
GO


