USE [Testdatabase]
GO
/****** Object:  StoredProcedure [dbo].[Get_User_Dept]    Script Date: 7/15/2022 11:50:30 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:           SJ
-- Create date: 5/17/2022
-- Description:      Procedure to pull the Department of the user, used limit what functions they can see 
-- =============================================
ALTER PROCEDURE [dbo].[Get_User_Dept] 

@fname nvarchar(50)
,@lname nvarchar(50)

AS
BEGIN
SET NOCOUNT ON;


SELECT DEPARTMENT FROM MANEX.dbo.USERS
WHERE FIRSTNAME = @fname AND NAME = @lname

--Test Note
END