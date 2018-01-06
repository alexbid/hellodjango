
su - postgres
psql


\list
\connect marketdb
\dt

select * from stockscreener_batch_run where "BBG" = 'AREVA.PA';

UPDATE public.stockscreener_batch_run
SET "isWorking" = False WHERE "BBG" = 'VIAD.PA';


select * from intraday where "bbg"='^FCHI' ORDER BY "Date" DESC LIMIT 10;
DELETE FROM stockscreener_calendar WHERE (CDR=%s) 


marketdb=# select distinct "CDR" from stockscreener_batch_run;
 CDR 
-----
 SE
 UK
 US
 HK
 IT
 BE
 FR
 AT
 GE
 BR
 SP
 JP
 SW
(13 rows)


