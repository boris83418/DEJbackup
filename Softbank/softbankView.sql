-- ™ˆœ›ß‘¶İ“I‹š¤
IF OBJECT_ID('SoftBankSummaryView', 'V') IS NOT NULL
    DROP VIEW SoftBankSummaryView;
	-- İšdàÕ“I”áŸ’†‘nŒšV“I‹š¤
GO
-- ‘nŒšV“I‹š¤
CREATE VIEW SoftBankSummaryView AS
SELECT 
    o.dej_Estimate_Number,
    o.order_date,
    o.actual_shipment_date,
    o.estimated_shipment_date,
    o.delivery_date,
    o.Desired_delivery_Date,
	DATEADD(DAY, p.standard_delivery_Time, o.order_date) AS standard_delivery_time,
    o.station_Name,
    o.Product_Name,
    p.customer_Model_Name,
    o.quantity,
    o.ordererlocation,
    o.person_in_charge,
    o.recipient,
    o.contact_Department_Name,
    o.Contact_Person,
    o.Contact_Address,
    o.Contactphone,
    o.ContactNotes,
    o.SO_NO,
    o.DN_NO,
    c.Customer_code,
	FORMAT(p.unitprice, 'C', 'ja-JP') AS unitprice, -- Ši®‰»ˆ×“úš¢
    FORMAT(p.unitprice * o.quantity, 'C', 'ja-JP') AS [Œ©Ï‚è], -- Ši®‰»ˆ×“úš¢
    FORMAT(p.unitprice * o.quantity * 1.1, 'C', 'ja-JP') AS [Œ©Ï‚è(¿‹ÅŠÜ)], -- Ši®‰»ˆ×“úš¢
	o.Invoice_Number

FROM 
    SoftBank_Data_orderinfo o
JOIN 
    SoftBank_Data_Productinfo p ON o.Product_Name = p.Delta_PartNO
JOIN 
    SoftBank_Data_CustomerCode c ON o.Recipient = c.ASP;
GO
-- ‘nŒšV“I‹š¤
	SELECT * 
FROM SoftBankSummaryView;