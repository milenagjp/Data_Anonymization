create procedure [random_from_set](@ref1 varchar(225), @column1 varchar(225), @ref2 varchar(225),@column2 varchar(225))
AS 
begin
declare @FullQuery nvarchar(max), @sql nvarchar(max)
SET NOCOUNT ON;   

	exec(N'SELECT * INTO [Anonymized_' + @ref1 + '] FROM '+@ref1+'')

	exec(N'UPDATE [Anonymized_' + @ref1 + '] SET ' + @column1 + ' = (select top 1 b.'+@column2+'
from '+@ref1+' as a 
join '+@ref2+' as b
on a.'+@column1+'=b.'+@column2+'
order by rand())')

SET NOCOUNT OFF; 
end