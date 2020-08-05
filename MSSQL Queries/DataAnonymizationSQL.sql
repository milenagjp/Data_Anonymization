CREATE PROCEDURE Data_Anonymization
@table varchar(225),
@column varchar(225),
@type varchar(225)
AS
SET NOCOUNT ON;  
begin
	
if (@type = 'None')
begin 
exec [none] @table=@table, @column=@column
end

if (@type = 'Omit')
begin 
exec omit @table=@table, @column=@column
end

if (@type = 'Default')
begin 
exec [default] @table=@table, @column=@column
end

if (@type = 'Random')
begin 
exec random @table=@table, @column=@column
end


if (@type = 'null')
begin 
exec [null] @table=@table, @column=@column
end

set nocount off
end


exec Data_Anonymization @table='HumanResources.EmployeePayHistory', @column='Rate',@type='Omit' --ok
exec Data_Anonymization @table='Sales.SalesOrderHeader', @column='CreditCardApprovalCode',@type='Null' --ok
exec Data_Anonymization @table='Sales.CreditCard', @column='CardNumber',@type='Random' -- random not working 
exec Data_Anonymization @table='Person.EmailAddress', @column='EmailAddress',@type='None' --ok
exec Data_Anonymization @table='Purchasing.Vendor', @column='ModifiedDate',@type='Default' --ok
exec [random_from_set] @ref1='Purchasing.PurchaseOrderHeader', @column1='EmployeeID', @ref2='HumanResources.Employee', @column2 = 'BusinessEntityID',@type='RandomFromSet' --rand() not generating randoms
exec Data_Anonymization @table='Production.TransactionHistory', @column='TransactionID',@type='Omit' --ok

select * from [Anonymized_Person.EmailAddress] --none
select * from [Anonymized_HumanResources.EmployeePayHistory] --omit
select * from [Anonymized_Production.TransactionHistory] --omit
select * from [Anonymized_Sales.SalesOrderHeader] --null
select * from [Anonymized_Purchasing.Vendor] --default
select * from [Anonymized_Purchasing.PurchaseOrderHeader] --random from set
select * from [Anonymized_Sales.CreditCard] --random


