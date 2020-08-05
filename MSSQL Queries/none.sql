create procedure [none](@table varchar(225), @column varchar(225))
AS 
begin
declare @sql nvarchar(max)
SET NOCOUNT ON;  

	exec(N'select * into [Anonymized_' + @table + '] from '+@table+'')

SET NOCOUNT OFF; 
end
go

drop procedure [none]

sp_helptext [none]

exec [none] @table='Person.EmailAddress', @column='EmailAddress'
go
