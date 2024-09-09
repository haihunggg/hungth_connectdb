DELETE FROM "MInvoice"."GatewayRequest"  WHERE "SendDate" < '2024-07-30';
DELETE FROM "MInvoice"."GatewayReponse" WHERE "SendDate" < '2024-07-30' AND "MLTDiep" = '999'