create procedure [random](@table varchar(225), @column varchar(225))
AS 
begin
DECLARE @i int,  @name nvarchar(max), @table_name nvarchar(max), @sql nvarchar(max), @max int
SET NOCOUNT ON;  
	EXEC('SELECT * INTO [#Anonymized_' + @table + '] FROM '+@table+'' )
	set @table_name = CONCAT('[#Anonymized_',@table,']')
	set @sql = N'select COUNT(*) from '+ @table  
	--set @max = exec (@sql)
	execute sp_executesql @sql, N'@max int OUTPUT', @max OUTPUT
	select @max = @max
	set @i=1
	SELECT @name = (STUFF ((SELECT ',' + COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS S WHERE S.TABLE_SCHEMA = @table AND S.TABLE_NAME = @column AND S.ORDINAL_POSITION IN(1)
ORDER BY S.ORDINAL_POSITION FOR XML PATH('')),1,1,''))
	while (@i <19118)
	begin
		EXEC ('update' +@table_name+' set ' + @column + ' = FLOOR(RAND()*(1000000-5+1)+5) where '+  @name+' = '+@i)
		set @i = @i +1
	end;
SET NOCOUNT OFF; 
end
GO


/*
drop procedure [random]


exec [random] @table='Sales.CreditCard', @column='CardNumber'
go

select * from [Anonymized_Sales.CreditCard] from Sales.CreditCard

DECLARE @i int, @max int, @name nvarchar(max)
set @max = (select COUNT(*) from [Anonymized_Sales.CreditCard])
print @max
set @i=1
SELECT @name = (STUFF ((SELECT ',' + COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS S WHERE S.TABLE_SCHEMA = 'Sales.CreditCard' AND S.TABLE_NAME = 'CardNumber' AND S.ORDINAL_POSITION IN(1)
ORDER BY S.ORDINAL_POSITION FOR XML PATH('')),1,1,''))

--EXEC ('SELECT ' + @name + ' FROM HumanResources.Employee')
 
 --select @name from HumanResources.Employee where @name = 1
while (@i < @max)
begin
	EXEC ('update [Anonymized_Sales.CreditCard] set NationalIDNumber = FLOOR(RAND()*(1000000-5+1)+5) where '+  @name+' = '+@i)
	set @i = @i +1
	
end;

select * from [#anonym]



drop table #anonym

select * from Sales.CreditCard+

declare @max int,@sql nvarchar(max), @table nvarchar(max)
set @table = 'Sales.CreditCard '
	set @sql = N'select COUNT(*) from '+ @table
	execute sp_executesql @sql, N'@max int OUTPUT', @max OUTPUT
	print @max
	--execute sp_executesql @sql, N'@max int OUTPUT', @max OUTPUT

	*/