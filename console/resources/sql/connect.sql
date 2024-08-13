SELECT  
    a."Name", 
    a."Value"
FROM "public"."AbpTenantConnectionStrings" a 
JOIN "AbpTenants" b 
on b."Id" = a."TenantId";


